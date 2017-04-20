#!/usr/bin/env bash

TEXT=$1
LEX=$2
OUT=$3

echo "$TEXT" | farcompilestrings --symbols=$LEX --unknown_symbol='<unk>' --generate_keys=1 --keep_symbols | farextract --filename_suffix='.fst' --filename_prefix="$OUT"
