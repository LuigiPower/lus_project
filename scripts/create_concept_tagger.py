#!/usr/bin/env python3
# Creates concept tagger trying to use some extra features for the counts
# Creates word to lemma transducer and lemma to concept transducer
# Output lexicon has words, lemmas and concepts
#
# Weights for the first transducer are based on the probability of the word having a certain lemma
# Weights for the second transducer are based on the probability of the lemma having a certain postag and concepttag

import sys
import math
from collections import Counter

train = sys.argv[1]
trainfeats = sys.argv[2]
lexfile = sys.argv[3]
outfile = sys.argv[4]
outwordtolemma = sys.argv[5]
cutoff = int(sys.argv[6]) # Determines minimum frequency of elements in lexicon

lemmas = {} # Values of this dictionary are a list of lemmas: a word can have multiple lemmas (ex.: 's --> has, is)
lemma_taglist = {}
counts_lemmatag = {}

counts_wordlemma = {}
counts_lemma = {}

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

            wordlemma = "%s %s" % (word, lemma)
            lemmatag = "%s %s" % (lemma, tag)
            if wordlemma not in counts_wordlemma:
                counts_wordlemma[wordlemma] = 1
            else:
                counts_wordlemma[wordlemma] += 1

            if lemma not in counts_lemma:
                counts_lemma[lemma] = 1
            else:
                counts_lemma[lemma] += 1

            if word not in lemmas:
                lemmas[word] = []

            if lemma not in lemmas[word]:
                lemmas[word].append(lemma)

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

            possiblelemmas = [word]
            if word in lemmas:
                possiblelemmas = lemmas[word]
            else:
                print("Word %s not in lemmas (feats dataset is wrong?) Ignoring...")
                continue

            #print("Word %s has lemmalist %s" % (word, possiblelemmas))
            for lemma in possiblelemmas:
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

# Create the lexicon with lemmas and concepts
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

## now create the transducer with the found weights
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


weights_wordlemma = {}

for k, v in counts_wordlemma.items():
    wordlemma = k.split()
    word = wordlemma[0]
    lemma = wordlemma[1]
    c1 = counts_wordlemma[k]
    c2 = counts_lemma[lemma]
    prob = (c1/c2)
    neglogprob = -math.log(prob)
    weights_wordlemma[k] = neglogprob

wordtolemmaautomata = [];

for k, v in lemmas.items():
    word = k
    for lemma in v:
        wordlemma = "%s %s" % (word, lemma)
        wordtolemmaautomata.append("0 0 %s %s %s" % (word, lemma, weights_wordlemma[wordlemma]))

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

