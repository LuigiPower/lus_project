#!/usr/bin/env bash

WORDTOLEMMA=$1
LEMMATOPOS=$2
POSTOCONCEPT=$3
MODEL=$4
FINAL=$5
LEX=$6

fstarcsort $WORDTOLEMMA > $WORDTOLEMMA.sort
fstarcsort $LEMMATOCONCEPT > $LEMMATOCONCEPT.sort
fstcompose $WORDTOLEMMA.sort $LEMMATOPOS.sort | fstcompose - $POSTOCONCEPT | fstcompose - $MODEL > $FINAL.fsa

#fstprint -isymbols=$LEX -osymbols=$LEX $FINAL.fsa
#fstdraw -isymbols=$LEX -osymbols=$LEX $MODEL.fsa | dot -Teps > $MODEL.eps
#open $MODEL.eps
