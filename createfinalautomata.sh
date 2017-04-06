#!/usr/bin/env bash

WORDTOLEMMA=$1
LEMMATOCONCEPT=$2
MODEL=$3
FINAL=$4
LEX=$5

fstarcsort $WORDTOLEMMA > $WORDTOLEMMA.sort
fstarcsort $LEMMATOCONCEPT > $LEMMATOCONCEPT.sort
fstcompose $WORDTOLEMMA.sort $LEMMATOCONCEPT.sort | fstcompose - $MODEL > $FINAL.fsa

#fstprint -isymbols=$LEX -osymbols=$LEX $FINAL.fsa
#fstdraw -isymbols=$LEX -osymbols=$LEX $MODEL.fsa | dot -Teps > $MODEL.eps
#open $MODEL.eps
