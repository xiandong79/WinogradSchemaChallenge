import nltk
import os
import sys

from nltk.tokenize import word_tokenize


def make_tags(sent):
    result = word_tokenize(sent)
    # print result
    return nltk.pos_tag(result)


tags = make_tags(
    "The city councilmen refused the demonstrators a permit because they feared violence.")
# print tags
# print tags[1][0]
# print tags[1][1]

from nltk.corpus import wordnet

syns1 = wordnet.synsets("COMP5211")
syns2 = wordnet.synsets("ugly")

print syns1

# wrong!  print syns1.wup_similarity(syns2)


dog = wordnet.synset('dog.n.01')

# print dog

# cb = wordnet.synset('cookbook.n.01')
# ib = wordnet.synset('instruction_book.n.01')
# cb.wup_similarity(ib)
# 0.9166666666666666
