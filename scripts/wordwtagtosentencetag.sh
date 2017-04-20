#!/usr/bin/env bash

data=$1
which=$2

cat $data | cut -f $which | sed 's/^ *$/#/g' | tr '\n' ' ' | tr '#' '\n' | sed 's/^ *//g;s/ *$//g'
