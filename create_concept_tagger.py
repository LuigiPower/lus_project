#!/usr/bin/env python3

import sys
import math
from collections import Counter

train = sys.argv[1]
trainfeats = sys.argv[2]
lexfile = sys.argv[3]
outfile = sys.argv[4]
outwordtolemma = sys.argv[5]

lemmas = {} # TODO Change the values of this dictionary to a list of lemmas: a word can have multiple lemmas (ex.: 's --> has, is)
lemma_taglist = {}
counts_lemmatag = {}

wordlist = []
lemmalist = []
taglist = []
conceptlist = []

with open(trainfeats, 'r') as f:
    content = f.readlines()
    for line in content:
        wordtaglemma = line.split()
        if len(wordtaglemma) > 0:
            word = wordtaglemma[0]
            tag = wordtaglemma[1]
            lemma = wordtaglemma[2]

            if tag not in taglist:
                taglist.append(tag)
            if lemma not in lemmalist:
                lemmalist.append(lemma)

            if word not in wordlist:
                wordlist.append(word)
            if lemma not in wordlist:
                wordlist.append(lemma)

            lemmatag = "%s %s" % (lemma, tag)
            lemmas[word] = lemma

            if lemmatag not in counts_lemmatag:
                counts_lemmatag[lemmatag] = 1
            else:
                counts_lemmatag[lemmatag] += 1

            if lemma not in lemma_taglist:
                lemma_taglist[lemma] = []
            if tag not in lemma_taglist[lemma]:
                lemma_taglist[lemma].append(tag)

# counts_lemmatag containts <lemma, pos tag> counts
counts_lemmatagconcept = {}
counts_tagconcept = {}

with open(train, 'r') as f:
    content = f.readlines()
    for line in content:
        wordconcept = line.split()
        if len(wordconcept) > 0:
            word = wordconcept[0]
            concept = wordconcept[1]

            if concept not in conceptlist:
                #print("Adding concept %s" % concept)
                conceptlist.append(concept)

            lemma = word
            if word in lemmas:
                lemma = lemmas[word]
            else:
                #print("Word %s not in lemmas (feats dataset is wrong?) Ignoring...")
                continue

            for tag in lemma_taglist[lemma]:
                lemmatagconcept = "%s %s %s" % (lemma, tag, concept)
                tagconcept = "%s %s" % (tag, concept)
                if lemmatagconcept not in counts_lemmatagconcept:
                    counts_lemmatagconcept[lemmatagconcept] = 1
                else:
                    counts_lemmatagconcept[lemmatagconcept] += 1

                if tagconcept not in counts_tagconcept:
                    counts_tagconcept[tagconcept] = 1
                else:
                    counts_tagconcept[tagconcept] += 1

#print(counts_lemmatag)
#print(counts_tagconcept)
#print(counts_lemmatagconcept)
#print(lemmalist)
#print(taglist)
#print(conceptlist)

# Create the lexicon with lemmas and concepts (TODO do I also need tags? if not, why not?)
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

## TODO now create the transducer with the found weights
#
## format:
## f t i o weight
## 0 0 a n 0.1
#
## So I need:
## 0 0 lemma concept P(lemma | tag, concept) = P(lemma, tag, concept) / P(tag, concept)
weights_lemmatagconcept = {}

for k, v in counts_lemmatagconcept.items():
    lemmatagconcept = k.split()
    lemma = lemmatagconcept[0]
    tag = lemmatagconcept[1]
    concept = lemmatagconcept[2]
    c1 = counts_lemmatagconcept[k]
    c2 = counts_tagconcept["%s %s" % (tag, concept)]
    prob = (c1/c2)
    neglogprob = -math.log(prob)
    weights_lemmatagconcept[k] = neglogprob

automata = []

for lemma in lemmalist:
    for tag in taglist:
        for concept in conceptlist:
            lemmatagconcept = "%s %s %s" % (lemma, tag, concept)
            if lemmatagconcept in weights_lemmatagconcept:
                weight = weights_lemmatagconcept[lemmatagconcept]
            else:
                continue

            if lemmatagconcept:
                automata.append("0 0 %s %s %s" % (lemma, concept, weight))

for concept in conceptlist:
    automata.append("0 0 <unk> %s %s" % (concept, -math.log(1/len(conceptlist)))) # TODO create different automata and run union

automata.append("0 0")

wordtolemmaautomata = [];

for k, v in lemmas.items():
    wordtolemmaautomata.append("0 0 %s %s 0" % (k, v))

for lemma in lemmalist:
    if lemma not in lemmas: #checks key (which is a word)
        wordtolemmaautomata.append("0 0 %s %s 0" % (lemma, lemma))

wordtolemmaautomata.append("0 0 <unk> <unk> 0")
wordtolemmaautomata.append("0 0")

#for lemma in lemmalist:
#    wordtolemmaautomata.append("0 0 <unk> %s %s" % (lemma, -math.log(1/len(lemmalist))))

with open(outfile, 'w') as f:
    for line in automata:
        f.write(line)
        f.write("\n")

with open(outwordtolemma, 'w') as f:
    for line in wordtolemmaautomata:
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
