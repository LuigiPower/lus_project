#!/usr/bin/env bash

INPUT=$1
LEX=$2
TAGGER=$3

TEMP="tempstring"

paste "P1/data/NLSPARQL.test.data" <(
    while read line
    do
        #echo "$line"
        ../automata/farstringtofsa.sh "$line" $LEX $TEMP > /dev/null
        #fstprint -isymbols=$LEX -osymbols=$LEX ${TEMP}1.fst
        #
        ./domodelcompose.sh ${TEMP}1.fst $TAGGER $LEX | cut -d$'\t' -f 4
    done < $INPUT
) > $TAGGER.output.txt

