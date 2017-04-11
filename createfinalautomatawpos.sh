#!/usr/bin/env bash

WORDTOLEMMA=$1
LEMMATOPOS=$2
POSTOCONCEPT=$3
MODEL=$4
LEX=$5

fstarcsort $WORDTOLEMMA > $WORDTOLEMMA.sort
fstarcsort $LEMMATOPOS > $LEMMATOPOS.sort
fstarcsort $POSTOCONCEPT > $POSTOCONCEPT.sort
fstcompose $WORDTOLEMMA.sort $LEMMATOPOS.sort > wordtopos.interm
fstcompose wordtopos.interm $POSTOCONCEPT.sort > wordtoconcept.interm
fstcompose wordtoconcept.interm $MODEL > $MODEL.final.fsa

#fstprint -isymbols=$LEX -osymbols=$LEX $FINAL.fsa
#fstdraw -isymbols=$LEX -osymbols=$LEX $MODEL.fsa | dot -Teps > $MODEL.eps
#open $MODEL.eps
