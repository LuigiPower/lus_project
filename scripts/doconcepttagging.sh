#!/usr/bin/env bash

INPUT=$1
LEX=$2
TAGGER=$3
TEST=$4
TEMP=$5

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

paste $TEST <(
    while read line
    do
        #echo "$line"
        $DIR/farstringtofsa.sh "$line" $LEX $TEMP > /dev/null
        #fstprint -isymbols=$LEX -osymbols=$LEX ${TEMP}1.fst

        $DIR/domodelcompose.sh ${TEMP}1.fst $TAGGER $LEX | cut -d$'\t' -f 4
    done < $INPUT
) > $TAGGER.output.txt

