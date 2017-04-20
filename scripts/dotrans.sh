#!/bin/bash

INLEX=$1
OUTLEX=$2
AUT=$3

fstcompile --isymbols=$INLEX --osymbols=$OUTLEX $AUT > $AUT.fsa
#fsttopsort $AUT.fsa $AUT.sorted.fsa
#fstprint -isymbols=$INLEX -osymbols=$OUTLEX $AUT.fsa
#fstdraw --isymbols=$INLEX -osymbols=$OUTLEX $AUT.fsa | dot -Teps > $AUT.eps

