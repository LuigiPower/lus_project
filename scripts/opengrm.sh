#!/bin/bash

input=$1
output=$2
lex=$3
order=$4
method=$5

farcompilestrings --symbols=$lex -keep_symbols=1 $input > $output$order.far
ngramcount --order=$order $output$order.far > $output$order.cnts
ngrammake --method=$method $output$order.cnts > $output-$method-$order.lm

#ngramrandgen $output$order.lm | farprintstrings
