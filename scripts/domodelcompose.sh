#!/usr/bin/env bash

INAUT=$1
AUT=$2
LEX=$3

fstcompose $INAUT $AUT | fstrmepsilon | fstshortestpath | fsttopsort > $AUT.short.fsa
#fstcompose $INAUT $WORDTOLEMMA | fstcompose - $LEMMATOCONCEPT | fstcompose - $MODEL | fstrmepsilon | fstshortestpath | fsttopsort > $MODEL.fsa

fstprint -isymbols=$LEX -osymbols=$LEX $AUT.short.fsa
#fstdraw -isymbols=$LEX -osymbols=$LEX $AUT.short.fsa | dot -Teps > $AUT.short.eps
#open $AUT.short.eps
