#!/usr/bin/env python3

import sys
import math
from collections import Counter

from utils import inc
from utils import calc_weights

train = sys.argv[1]
outfile = sys.argv[2]
splitmethod = sys.argv[3] # 1 = after '.', 2 = after '-', 3 = between '-' and '.'

generalizations = []

with open(train) as trainfile:
    content = trainfile.readlines()
    for line in content:
        wordconcept = line.split()

        if len(wordconcept) == 0:
            continue

        word = wordconcept[0]
        concept = wordconcept[1]

        splitted = concept.split('.')
        if len(splitted) <= 1:
            # It's an out of concept tag
            g = word
        else:
            if splitmethod == "1":
                g = "$%s" % splitted[1]
            elif splitmethod == "2":
                g = "$%s" % concept.split('-')[1]
            elif splitmethod == "3":
                g = "$%s" % splitted[0].split('-')[1]
            #print(g)


        generalizations.append("%s\t%s\t%s" % (word, concept, g))

#print(generalizations)

with open(outfile, 'w') as f:
    for line in generalizations:
        f.write(line)
        f.write("\n")

