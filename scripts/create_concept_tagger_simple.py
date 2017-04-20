#!/usr/bin/env python3

import sys
import math
from collections import Counter

train = sys.argv[1]
trainfeats = sys.argv[2]
lexfile = sys.argv[3]
outfile = sys.argv[4]

# p(w, l, p | c) = C(w, l, p, c) / C(c)

counts_wlpc = {}
counts_c = {}
wordlist = []
lemmas = {}
tags = {}
concepts = {}
conceptlist = []

with open(train) as trainfile, open(trainfeats) as featsfile:
    for x, y in zip(trainfile, featsfile):
        wordconcept = x.split()
        wordtaglemma = y.split()
        print("{0}\t{1}".format(x, y))

        if len(wordconcept) == 0:
            continue

        word = wordconcept[0]
        concept = wordconcept[1]
        tag = wordtaglemma[1]
        lemma = wordtaglemma[2]

        wlpc = "%s %s %s %s" % (word, lemma, tag, concept)

        if word not in wordlist:
            wordlist.append(word)
        if concept not in conceptlist:
            conceptlist.append(concept)

        if wlpc not in counts_wlpc:
            counts_wlpc[wlpc] = 1
        else:
            counts_wlpc[wlpc] += 1

        if concept not in counts_c:
            counts_c[concept] = 1
        else:
            counts_c[concept] += 1

        if word not in lemmas:
            lemmas[word] = []
        if lemma not in lemmas[word]:
            lemmas[word].append(lemma)

        if word not in tags:
            tags[word] = []
        if tag not in tags[word]:
            tags[word].append(tag)

        if word not in concepts:
            concepts[word] = []
        if concept not in concepts[word]:
            concepts[word].append(concept)



# Create the lexicon with words and concepts
inserted_tokens = {}

lex = ["<eps> 0"]

current = 1

for word in wordlist:
    lex.append("%s %d" % (word, current))
    current += 1

for concept in conceptlist:
    lex.append("%s %d" % (concept, current))
    current += 1

lex.append("<unk> %d" % current)

#print(lex)

with open(lexfile, 'w') as f:
    for line in lex:
        f.write(line)
        f.write("\n")


# Create the automata
weights_wlpc = {}

for k, v in counts_wlpc.items():
    wlpc = k.split()
    concept = wlpc[3]
    c1 = v
    c2 = counts_c[concept]
    prob = (c1/c2)
    neglogprob = -math.log(prob)
    weights_wlpc[k] = neglogprob;

automata = []

for k, weight in weights_wlpc.items():
    wlpc = k.split()
    word = wlpc[0]
    lemma = wlpc[1]
    concept = wlpc[3]
    automata.append("0 0 %s %s %s" % (lemma, concept, weight))

#for word in wordlist:
#    for lemma in lemmas[word]:
#        for tag in tags[word]:
#            for concept in concepts[word]:
#                wlpc = "%s %s %s %s" % (word, lemma, tag, concept)
#                if wlpc in weights_wlpc:
#                    weight = weights_wlpc[wlpc]
#                    automata.append("0 0 %s %s %s" % (word, concept, weight))

for concept in conceptlist:
    automata.append("0 0 <unk> %s %s" % (concept, -math.log(1/len(conceptlist))))

automata.append("0 0")

with open(outfile, 'w') as f:
    for line in automata:
        f.write(line)
        f.write("\n")

