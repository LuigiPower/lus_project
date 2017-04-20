#!/bin/bash

function usage {
    echo ""
    echo "Usage:"
    echo "create_and_run.sh -e evalscript.pl -i input.txt [-f input.feats.txt] -t test.txt -b builddir -s tagger [-m method] [-o order] [-c number] [-n]"
    echo "Where tagger is one of nofeats, 2step, 2stepgivenc, 3step, gen_nofeats"
    echo ""
    exit 1
}

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -e|--evalscript)
            EVALSCRIPT="$2"
            shift
            ;;
        -i|--training)
            TRAIN="$2"
            TRAINNAME=$(basename $TRAIN)
            shift
            ;;
        -f|--feats)
            FEATS="$2"
            FEATSNAME=$(basename $FEATS)
            shift
            ;;
        -t|--test)
            TEST="$2"
            TESTNAME=$(basename $TEST)
            shift
            ;;
        -b|--builddir)
            OUTDIR="$2"
            OUTNAME=$(basename $OUTDIR)
            shift
            ;;
        -m|--method)
            METHOD="$2"
            shift
            ;;
        -o|--order)
            ORDER="$2"
            shift
            ;;
        -c|--cutoff)
            CUTOFF="$2"
            shift
            ;;
        -s|--tagger)
            TAGGER="$2"
            shift
            ;;
        -n|--skiptagging)
            SKIP="skip"
            ;;
        -j|--split)
            SPLIT="$2"
            shift
            ;;
        *)
            # unknown
            usage
            ;;
    esac
    shift
done

if [ -z "$TRAIN" ]
then
    usage
fi
if [ -z "$OUTDIR" ]
then
    usage
fi
if [ -z "$TEST" ]
then
    usage
fi
if [ -z "$EVALSCRIPT" ]
then
    usage
fi


if [ -z "$CUTOFF" ]
then
    CUTOFF=0
fi

if [ -z "$METHOD" ]
then
    METHOD=witten_bell
fi

if [ -z "$SPLIT" ]
then
    SPLIT=1
fi

if [ -z "$ORDER" ]
then
    ORDER=3
fi

mkdir -p $OUTDIR

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case $TAGGER in
    nofeats)
        python3 $DIR/create_concept_tagger_naive.py $TRAIN $OUTDIR/nofeats.lex $OUTDIR/nofeats.txt $CUTOFF
        $DIR/dotrans.sh $OUTDIR/nofeats.lex $OUTDIR/nofeats.lex $OUTDIR/nofeats.txt
        $DIR/wordwtagtosentencetag.sh $TRAIN 2 > $OUTDIR/conceptsentences.txt
        $DIR/wordwtagtosentencetag.sh $TEST 1 > $OUTDIR/testsentences.txt
        $DIR/opengrm.sh $OUTDIR/conceptsentences.txt $OUTDIR/conceptmodel $OUTDIR/nofeats.lex $ORDER $METHOD
        fstarcsort $OUTDIR/nofeats.txt.fsa > $OUTDIR/nofeats.txt.sorted.fsa
        fstcompose $OUTDIR/nofeats.txt.sorted.fsa $OUTDIR/conceptmodel-$METHOD-$ORDER.lm > $OUTDIR/nofeats-$METHOD-$ORDER.fsa

        if [ -z "$SKIP" ]
        then
            echo "Doing concept tagging..."
            $DIR/doconcepttagging.sh $OUTDIR/testsentences.txt $OUTDIR/nofeats.lex $OUTDIR/nofeats-$METHOD-$ORDER.fsa $TEST $OUTDIR/nofeatstemp.far
        fi
        RESULT=$OUTDIR/nofeats-$METHOD-$ORDER.fsa.output.txt
        ;;
    2step)
        if [ -z "$FEATS" ]
        then
            usage
        fi
        python3 $DIR/create_concept_tagger.py $TRAIN $FEATS $OUTDIR/2step.lex $OUTDIR/2step.txt $OUTDIR/2step_wordtolemma.txt $CUTOFF
        $DIR/dotrans.sh $OUTDIR/2step.lex $OUTDIR/2step.lex $OUTDIR/2step.txt
        $DIR/dotrans.sh $OUTDIR/2step.lex $OUTDIR/2step.lex $OUTDIR/2step_wordtolemma.txt
        $DIR/wordwtagtosentencetag.sh $TRAIN 2 > $OUTDIR/conceptsentences.txt
        $DIR/wordwtagtosentencetag.sh $TEST 1 > $OUTDIR/testsentences.txt
        $DIR/opengrm.sh $OUTDIR/conceptsentences.txt $OUTDIR/conceptmodel $OUTDIR/2step.lex $ORDER $METHOD
        $DIR/createfinalautomata.sh $OUTDIR/2step_wordtolemma.txt.fsa $OUTDIR/2step.txt.fsa $OUTDIR/conceptmodel-$METHOD-$ORDER.lm $OUTDIR/2step-$METHOD-$ORDER.fsa $OUTDIR/2step.lex

        if [ -z "$SKIP" ]
        then
            echo "Doing concept tagging..."
            $DIR/doconcepttagging.sh $OUTDIR/testsentences.txt $OUTDIR/2step.lex $OUTDIR/2step-$METHOD-$ORDER.fsa $TEST $OUTDIR/2steptemp.far
        fi
        RESULT=$OUTDIR/2step-$METHOD-$ORDER.fsa.output.txt
        ;;
    2stepgivenc)
        if [ -z "$FEATS" ]
        then
            usage
        fi
        python3 $DIR/create_concept_tagger_givenc.py $TRAIN $FEATS $OUTDIR/2step_givenc.lex $OUTDIR/2step_givenc.txt $OUTDIR/2step_givenc_wordtolemma.txt $CUTOFF
        $DIR/dotrans.sh $OUTDIR/2step_givenc.lex $OUTDIR/2step_givenc.lex $OUTDIR/2step_givenc.txt
        $DIR/dotrans.sh $OUTDIR/2step_givenc.lex $OUTDIR/2step_givenc.lex $OUTDIR/2step_givenc_wordtolemma.txt
        $DIR/wordwtagtosentencetag.sh $TRAIN 2 > $OUTDIR/conceptsentences.txt
        $DIR/wordwtagtosentencetag.sh $TEST 1 > $OUTDIR/testsentences.txt
        $DIR/opengrm.sh $OUTDIR/conceptsentences.txt $OUTDIR/conceptmodel $OUTDIR/2step_givenc.lex $ORDER $METHOD
        $DIR/createfinalautomata.sh $OUTDIR/2step_givenc_wordtolemma.txt.fsa $OUTDIR/2step_givenc.txt.fsa $OUTDIR/conceptmodel-$METHOD-$ORDER.lm $OUTDIR/2step_givenc-$METHOD-$ORDER.fsa $OUTDIR/2step_givenc.lex

        if [ -z "$SKIP" ]
        then
            echo "Doing concept tagging..."
            $DIR/doconcepttagging.sh $OUTDIR/testsentences.txt $OUTDIR/2step_givenc.lex $OUTDIR/2step_givenc-$METHOD-$ORDER.fsa $TEST $OUTDIR/2step_givenctemp.far
        fi
        RESULT=$OUTDIR/2step_givenc-$METHOD-$ORDER.fsa.output.txt
        ;;
    3step)
        if [ -z "$FEATS" ]
        then
            usage
        fi
        python3 $DIR/create_wordtolemma_lemmatopos_postoconcept_tagger.py $TRAIN $FEATS $OUTDIR/3step.lex $OUTDIR/3step_wordtolemma.txt $OUTDIR/3step_lemmatopos.txt $OUTDIR/3step_postoconcept.txt $CUTOFF
        $DIR/dotrans.sh $OUTDIR/3step.lex $OUTDIR/3step.lex $OUTDIR/3step_wordtolemma.txt
        $DIR/dotrans.sh $OUTDIR/3step.lex $OUTDIR/3step.lex $OUTDIR/3step_lemmatopos.txt
        $DIR/dotrans.sh $OUTDIR/3step.lex $OUTDIR/3step.lex $OUTDIR/3step_postoconcept.txt
        $DIR/wordwtagtosentencetag.sh $TRAIN 2 > $OUTDIR/conceptsentences.txt
        $DIR/wordwtagtosentencetag.sh $TEST 1 > $OUTDIR/testsentences.txt
        $DIR/opengrm.sh $OUTDIR/conceptsentences.txt $OUTDIR/conceptmodel $OUTDIR/3step.lex $ORDER $METHOD
        $DIR/createfinalautomatawpos.sh $OUTDIR/3step_wordtolemma.txt.fsa $OUTDIR/3step_lemmatopos.txt.fsa $OUTDIR/3step_postoconcept.txt.fsa $OUTDIR/conceptmodel-$METHOD-$ORDER.lm $OUTDIR/3step-$METHOD-$ORDER.fsa $OUTDIR/3step.lex

        if [ -z "$SKIP" ]
        then
            echo "Doing concept tagging..."
            $DIR/doconcepttagging.sh $OUTDIR/testsentences.txt $OUTDIR/3step.lex $OUTDIR/3step-$METHOD-$ORDER.fsa $TEST $OUTDIR/3steptemp.far
        fi
        RESULT=$OUTDIR/3step-$METHOD-$ORDER.fsa.output.txt
        ;;
    gen_nofeats)
        python3 $DIR/create_generalizations.py $TRAIN $OUTDIR/training.generalized.txt $SPLIT
        python3 $DIR/create_concept_tagger_generalization.py $OUTDIR/training.generalized.txt $OUTDIR/genlex.lex $OUTDIR/wordtogen.txt $OUTDIR/gentoconcept.txt $CUTOFF
        $DIR/dotrans.sh $OUTDIR/genlex.lex $OUTDIR/genlex.lex $OUTDIR/wordtogen.txt
        $DIR/dotrans.sh $OUTDIR/genlex.lex $OUTDIR/genlex.lex $OUTDIR/gentoconcept.txt
        $DIR/wordwtagtosentencetag.sh $OUTDIR/training.generalized.txt 2 > $OUTDIR/conceptsentences.txt
        $DIR/wordwtagtosentencetag.sh $TEST 1 > $OUTDIR/testsentences.txt
        $DIR/opengrm.sh $OUTDIR/conceptsentences.txt $OUTDIR/conceptmodel $OUTDIR/genlex.lex $ORDER $METHOD
        #fstarcsort $OUTDIR/nofeats.txt.fsa > $OUTDIR/nofeats.txt.sorted.fsa
        #fstcompose $OUTDIR/nofeats.txt.sorted.fsa $OUTDIR/conceptmodel-$METHOD-$ORDER.lm > $OUTDIR/nofeats-$METHOD-$ORDER.fsa
        $DIR/createfinalautomata.sh $OUTDIR/wordtogen.txt.fsa $OUTDIR/gentoconcept.txt.fsa $OUTDIR/conceptmodel-$METHOD-$ORDER.lm $OUTDIR/wordtogentoconcept-$METHOD-$ORDER.fsa $OUTDIR/genlex.lex

        if [ -z "$SKIP" ]
        then
            echo "Doing concept tagging..."
            $DIR/doconcepttagging.sh $OUTDIR/testsentences.txt $OUTDIR/genlex.lex $OUTDIR/wordtogentoconcept-$METHOD-$ORDER.fsa $TEST $OUTDIR/wordtogentoconcepttemp.far
        fi
        RESULT=$OUTDIR/wordtogentoconcept-$METHOD-$ORDER.fsa.output.txt
        ;;
    *)
        usage
        ;;
esac

perl $EVALSCRIPT -d '\t' < $RESULT > $RESULT.result
