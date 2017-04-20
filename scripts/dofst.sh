#!/bin/bash

LEX=$1
AUT=$2

fstcompile --acceptor --isymbols=$LEX $AUT > $AUT.fsa
fsttopsort $AUT.fsa $AUT.sorted.fsa
fstprint --acceptor -isymbols=$LEX $AUT.fsa
fstdraw --acceptor --isymbols=$LEX $AUT.fsa | dot -Teps > $AUT.eps

