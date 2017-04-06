#!/usr/bin/env bash

WORDTOLEMMA=$1
LEMMATOPOS=$2
POSTOCONCEPT=$3
MODEL=$4
FINAL=$5
LEX=$6

fstarcsort $WORDTOLEMMA > $WORDTOLEMMA.sort
fstarcsort $LEMMATOPOS > $LEMMATOPOS.sort
fstarcsort $POSTOCONCEPT > $POSTOCONCEPT.sort
fstcompose $WORDTOLEMMA.sort $LEMMATOPOS.sort > build/wordtopos.interm
fstcompose build/wordtopos.interm $POSTOCONCEPT.sort > build/wordtoconcept.interm
fstcompose build/wordtoconcept.interm $MODEL > $FINAL.fsa

#fstprint -isymbols=$LEX -osymbols=$LEX $FINAL.fsa
#fstdraw -isymbols=$LEX -osymbols=$LEX $MODEL.fsa | dot -Teps > $MODEL.eps
#open $MODEL.eps
