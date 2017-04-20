#!/usr/bin/env python3
# Creates concept tagger without using any extra features for the counts
# Creates word to concept transducer
# Output lexicon has words and concepts
#
# Weights for the transducer are based on the probability of the word having a certain concept

import sys
import math
from collections import Counter

from utils import inc
from utils import calc_weights

train = sys.argv[1]
lexfile = sys.argv[2]
outfile = sys.argv[3]
cutoff = int(sys.argv[4])

# p(w | c) = C(w, c) / C(c)

all_words = set()
all_concepts = set()

counts_wc = {}
counts_c = {}
counts_w = {}

with open(train) as trainfile:
    content = trainfile.readlines()
    for line in content:
        wordconcept = line.split()

        if len(wordconcept) == 0:
            continue

        word = wordconcept[0]
        concept = wordconcept[1]

        wc = "%s %s" % (word, concept)

        all_words.add(word)
        all_concepts.add(concept)

        inc(counts_wc, wc)
        inc(counts_c, concept)
        inc(counts_w, word)

#print(counts_wc)
#print(counts_c)

# Create the lexicon with words and concepts
inserted_tokens = {}

lex = ["<eps> 0"]

current = 1

def frequency_cutoff(word):
    return counts_w[word] > cutoff

all_words = set(filter(frequency_cutoff, all_words))

for word in all_words:
    lex.append("%s %d" % (word, current))
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
weights_wc = {}

#calc_weights(weights_wc, counts_wc, counts_c)

for k, v in counts_wc.items():
    wc = k.split()
    word = wc[0]
    concept = wc[1]
    if counts_w[word] <= cutoff:
        continue
    c1 = v
    c2 = counts_c[concept]
    prob = (c1/c2)
    #print("Count c1: %d c2: %d prob: %f" % (c1, c2, prob))
    neglogprob = -math.log(prob)
    weights_wc[k] = neglogprob;


automata = []

for k, weight in weights_wc.items():
    wc = k.split()
    word = wc[0]
    concept = wc[1]
    automata.append("0 0 %s %s %s" % (word, concept, weight))

#for word in wordlist:
#    for lemma in lemmas[word]:
#        for tag in tags[word]:
#            for concept in concepts[word]:
#                wlpc = "%s %s %s %s" % (word, lemma, tag, concept)
#                if wlpc in weights_wlpc:
#                    weight = weights_wlpc[wlpc]
#                    automata.append("0 0 %s %s %s" % (word, concept, weight))

for concept in all_concepts:
    #automata.append("0 0 <unk> %s %s" % (concept, 0))
    automata.append("0 0 <unk> %s %s" % (concept, -math.log(1/len(all_concepts))))
    #automata.append("0 0 <unk> %s %s" % (concept, -math.log(counts_c[concept]/len(all_concepts))))

automata.append("0 0")

with open(outfile, 'w') as f:
    for line in automata:
        f.write(line)
        f.write("\n")

