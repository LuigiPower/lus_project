#!/usr/bin/env python3

import sys
import math
from collections import Counter

from utils import inc
from utils import calc_weights

train = sys.argv[1]
outword = sys.argv[2]
outconc = sys.argv[3]
outgen1 = sys.argv[4]
outgen2 = sys.argv[5]
outgen3 = sys.argv[6]

all_words = set()
all_concepts = set()

counts_w = {}
counts_c = {}
counts_g1 = {}
counts_g2 = {}
counts_g3 = {}

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
            inc(counts_g1, g)
            inc(counts_g2, g)
            inc(counts_g3, g)
        else:
            g1 = "$%s" % splitted[1]
            g2 = "$%s" % concept.split('-')[1]
            g3 = "$%s" % splitted[0].split('-')[1]
            inc(counts_g1, g1)
            inc(counts_g2, g2)
            inc(counts_g3, g3)
            concept = concept.split('-')[1]

        inc(counts_w, word)
        inc(counts_c, concept)

#print(generalizations)

with open(outword, 'w') as f:
    for k, v in counts_w.items():
        f.write("%s %s" % (k, v))
        f.write("\n")

with open(outconc, 'w') as f:
    for k, v in counts_c.items():
        f.write("%s %s" % (k, v))
        f.write("\n")

with open(outgen1, 'w') as f:
    for k, v in counts_g1.items():
        f.write("%s %s" % (k, v))
        f.write("\n")

with open(outgen2, 'w') as f:
    for k, v in counts_g2.items():
        f.write("%s %s" % (k, v))
        f.write("\n")

with open(outgen3, 'w') as f:
    for k, v in counts_g3.items():
        f.write("%s %s" % (k, v))
        f.write("\n")

