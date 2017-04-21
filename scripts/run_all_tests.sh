#!/bin/bash

TRAIN=$1
FEATS=$2
TEST=$3
EVAL=$4
FOLDER=$5

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# 2step 2stepgivenc 3step gen_nofeats
for METHOD in witten_bell absolute kneser_ney katz presmoothed unsmoothed
do
    for ORDER in 1
    do
        for CUTOFF in 0
        do
            for TAGGER in nofeats
            do
                $DIR/create_and_run.sh -i $TRAIN -f $FEATS -t $TEST -s $TAGGER -b $FOLDER/$TAGGER-$METHOD-$ORDER-cutoff_$CUTOFF -j 3 -e $EVAL -c $CUTOFF -m $METHOD -o $ORDER
            done
        done
    done
done
