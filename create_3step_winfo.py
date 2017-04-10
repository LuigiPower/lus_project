#!/usr/bin/env python3

import sys
import math
from collections import Counter

train = sys.argv[1]
trainfeats = sys.argv[2]
lexfile = sys.argv[3]
outwordtolemma = sys.argv[4]
outlemmatopos = sys.argv[5]
outpostoconcept = sys.argv[6]

lemmas = {}
lemma_taglist = {}

all_words = set()
all_lemmas = set()
all_tags = set()
all_concepts = set()

# counts_lemmatag containts <lemma, pos tag> counts
c_wl = {}
c_l = {}

c_wlp = {}
c_p = {}

c_wlpc = {}
c_c = {}

def inc(dic, key):
    if key not in dic:
        dic[key] = 1
    else:
        dic[key] += 1

with open(train) as trainfile, open(trainfeats) as featsfile:
    for x, y in zip(trainfile, featsfile):
        wordconcept = x.split()
        wordtaglemma = y.split()
        print("{0}\t{1}".format(x, y))

        if len(wordconcept) == 0:
            continue

        w = wordconcept[0]
        l = wordtaglemma[2]
        p = wordtaglemma[1]
        c = wordconcept[1]

        all_words.add(w)
        all_lemmas.add(l)
        all_tags.add(p)
        all_concepts.add(c)

        wl = "%s %s" % (w, l)
        wlp = "%s %s %s" % (w, l p)
        wlpc = "%s %s %s %s" % (w, l, p, c)

        inc(c_wl, wl)
        inc(c_l, l)

        inc(c_wlp, wlp)
        inc(c_p, p)

        inc(wlpc, wlpc)
        inc(c_c, c)

# Create the lexicon with words, lemmas, tags, concepts
inserted_tokens = {}

lex = ["<eps> 0"]

current = 1

for word in all_words:
    lex.append("%s %d" % (word, current))
    current += 1

for lemma in (all_lemmas - all_words):
    lex.append("%s %d" % (lemma, current))
    current += 1

for tag in all_tags:
    lex.append("%s %d" % (tag, current))
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


## Now Compute weights
def calc_weights(wdic, cdic, call):
    for k, v in wdic.items():
        vals = k.split()
        target = vals[-1]
        c1 = v
        c2 = call[target]
        p = -math.log(c1/c2)
        wdic[k] = p


w_wl = {}
w_wlp = {}
w_wlpc = {}

calc_weights(w_wl, c_wl, c_l)
calc_weights(w_wlp, c_wlp, c_p)
calc_weights(w_wlpc, c_wlpc, c_c)

## Now create the transducers with the found weights
#
## format:
## f t i o weight
## 0 0 a n 0.1
#
## So I need:
## 0 0 lemma concept P(lemma | tag, concept) = P(lemma, tag, concept) / P(tag, concept)
w_to_wl = []
wl_to_wlp = []
wlp_to_c = []

for k in w_wl:
    wl = k.split()
    w = wl[0]
    l = wl[1]
    w_to_wl.append("0 0 %s %s %s" % (w, "%s$%s" % (w, l), w_wl[k]))

for k in w_wlp:
    wlp = k.split()
    w = wl[0]
    l = wl[1]
    p = wl[2]
    wl_to_wlp.append("0 0 %s %s %s" % ("%s$%s" % (w, l), "%s$%s$%s" % (w, l, p), w_wlp[k]))

for k in w_wlpc:
    wlpc = k.split()
    w = wl[0]
    l = wl[1]
    p = wl[2]
    c = wl[3]
    wlp_to_c.append("0 0 %s %s %s" % ("%s$%s$%s" % (w, l, p), "%s" % (c), w_wlpc[k]))

w_to_l.append("0 0")
wl_to_p.append("0 0")
wlp_to_c.append("0 0")

## Write automatas to file
with open(outwordtolemma, 'w') as f:
    for line in wordtolemmaautomata:
        f.write(line)
        f.write("\n")

with open(outlemmatopos, 'w') as f:
    for line in lemmatopos:
        f.write(line)
        f.write("\n")

with open(outpostoconcept, 'w') as f:
    for line in postoconcept:
        f.write(line)
        f.write("\n")



#print(automata)

#for k, v in tagcount.items():
#    tagtotal = tagtotal + v
#
#for k, v in tagcount.items():
#    tagprobabilities[k] = v / tagtotal
#
#print(tagprobabilities)
#print(word_conditioned)
#
#

#
#automata = list()
#unkautomata = list()
#
#for word in wordlist:
#    for tag in taglist:
#        wordwtag = "%s\t%s\n" % (word, tag)
#        if wordwtag in word_conditioned:
#            weight = -math.log(word_conditioned[wordwtag])
#            automata.append("0 0 %s %s %s" % (word, tag, weight))
#
#for tag in taglist:
#    unkautomata.append("0 0 <unk> %s %s" % (tag, (1/len(taglist))))
#    automata.append("0 0 <unk> %s %s" % (tag, (1/len(taglist))))
#
#automata.append("0 0")
#unkautomata.append("0 0")
#
#print(automata)
#print(unkautomata)
#
#with open(outfile, 'w') as f:
#    for line in automata:
#        f.write(line)
#        f.write("\n")
#
#unkfile = outfile + "unk"
#
#with open(unkfile, 'w') as f:
#    for line in unkautomata:
#        f.write(line)
#        f.write("\n")
