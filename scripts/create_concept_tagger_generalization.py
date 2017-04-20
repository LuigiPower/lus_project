#!/usr/bin/env python3
# Creates concept tagger without using any extra features for the counts
# Creates word to generalization and generalization to concept transducer
# Output lexicon has words, generalizations and concepts
#
# Weights for the first transducer are based on the probability of the word having a certain generalization
# Weights for the second transducer are based on the probability of the generalization having a certain concept

import sys
import math
from collections import Counter

from utils import inc
from utils import calc_weights

train = sys.argv[1]
lexfile = sys.argv[2]
wordtogen = sys.argv[3]
gentoconcept = sys.argv[4]
cutoff = int(sys.argv[5])

# p(w | g) = C(w, g) / C(g)
# p(g | c) = C(g, c) / C(c)

all_words = set()
all_generalize = set()
all_concepts = set()

total = 0

counts_wg = {}
counts_gc = {}
counts_w = {}
counts_c = {}
counts_g = {}

with open(train) as trainfile:
    content = trainfile.readlines()
    for line in content:
        wordconcept = line.split()

        if len(wordconcept) == 0:
            continue

        word = wordconcept[0]
        concept = wordconcept[1]
        generalize = wordconcept[2]

        wg = "%s %s" % (word, generalize)
        gc = "%s %s" % (generalize, concept)

        all_words.add(word)
        all_generalize.add(generalize)
        all_concepts.add(concept)

        inc(counts_wg, wg)
        inc(counts_gc, gc)
        inc(counts_w, word)
        inc(counts_c, concept)
        inc(counts_g, generalize)

        total += 1

# Create the lexicon with words and concepts
inserted_tokens = {}

lex = ["<eps> 0"]

current = 1

def frequency_cutoff(word):
    return counts_w[word] > cutoff

def inverse_cutoff(word):
    return counts_w[word] <= cutoff

to_remove = set(filter(inverse_cutoff, all_words))
all_words = all_words - to_remove

for word in all_words:
    lex.append("%s %d" % (word, current))
    current += 1

for generalize in all_generalize:
    if generalize not in to_remove:
        lex.append("%s %d" % (generalize, current))
    current += 1


for concept in all_concepts:
    lex.append("%s %d" % (concept, current))
    current += 1

lex.append("<unk> %d" % current)

#print(lex)

with open(lexfile, 'w') as f:
    for line in lex:
        f.write(line)
        f.write("\n")


# Create the automata
weights_wg = {}
weights_gc = {}

#calc_weights(weights_wc, counts_wc, counts_c)

for k, v in counts_wg.items():
    wg = k.split()
    generalize = wg[1]
    word = wg[0]
    if counts_w[word] <= cutoff:
        continue
    c1 = v
    c2 = counts_g[generalize]
    prob = (c1/c2)
    neglogprob = -math.log(prob)
    weights_wg[k] = neglogprob;

for k, v in counts_gc.items():
    gc = k.split()
    generalize = gc[0]
    concept = gc[1]
    if generalize in to_remove:
        continue
    c1 = v
    c2 = counts_c[concept]
    prob = (c1/c2)
    neglogprob = -math.log(prob)
    weights_gc[k] = neglogprob;


automata_wg = []
automata_gc = []

for k, weight in weights_wg.items():
    wg = k.split()
    word = wg[0]
    generalize = wg[1]
    automata_wg.append("0 0 %s %s %s" % (word, generalize, weight))

automata_wg.append("0 0 <unk> <unk> 0")

#for generalize in all_generalize:
    #automata_wg.append("0 0 <unk> %s %s" % (generalize, -math.log(counts_g[generalize]/total)))

for k, weight in weights_gc.items():
    gc = k.split()
    generalize = gc[0]
    concept = gc[1]
    automata_gc.append("0 0 %s %s %s" % (generalize, concept, weight))

for concept in all_concepts:
    #automata_gc.append("0 0 <unk> %s %s" % (concept, 0))
    #automata_gc.append("0 0 <unk> %s %s" % (concept, -math.log(1/len(all_concepts))))
    automata_gc.append("0 0 <unk> %s %s" % (concept, -math.log(counts_c[concept]/total)))

automata_wg.append("0 0")
automata_gc.append("0 0")

with open(wordtogen, 'w') as f:
    for line in automata_wg:
        f.write(line)
        f.write("\n")

with open(gentoconcept, 'w') as f:
    for line in automata_gc:
        f.write(line)
        f.write("\n")

