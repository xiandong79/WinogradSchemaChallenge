##############################################################
#####           Answer by machine learning               #####
#####    1. define a feature vector for each question    #####
#####        2.  train a model using SVM                 #####
#####              Author: Xiandong QI                   #####
#####              Time: 2017-11-12                      #####
##############################################################

import os
import xml.etree.ElementTree
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from sklearn import svm

# make tags for each sentence


def make_tags(sentence):
    text = word_tokenize(sentence)
    return nltk.pos_tag(text)


# define the tags
DETERMINER = ['DT']
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
ADJECTIVE = ['JJ', 'JJR', 'JJS']
NEGATION = ["n't", 'not']


def is_verb(tup):
    for v in VERBS:
        if tup[1] == v:
            return v
    return False


def is_adj(tup):
    for a in ADJECTIVE:
        if tup[1] == a:
            return a
    return False


def is_negative(tup):
    if tup[1] == 'RB':
        for ne in NEGATION:
            if tup[0] == ne:
                return True
    return False


def is_negative_from_list(word_list):
    for t in word_list:
        if is_negative(t):
            return True
    return False


def is_deter(tup):
    for d in DETERMINER:
        if tup[1] == d:
            return d
    return False

# get the similarity of two key word extracted from two clauses seperately


def get_sim_value(word1, word2):
    synsets1 = wordnet.synsets(word1)
    synsets2 = wordnet.synsets(word2)
    sim_value = 0
    if (len(synsets1) == 0 or len(synsets2) == 0):
        return 0

    count = 1
    for lemma1 in synsets1:
        for lemma2 in synsets2:
            if lemma1.wup_similarity(lemma2) is None:
                sim_value = sim_value + 0
            else:
                sim_value = sim_value + lemma1.wup_similarity(lemma2)
                count = count + 1

    # print float(sim_value) / count
    return float(sim_value) / count

# extract feature vector for one sentence/question


def extract_feature(sentence1, sentence2):

    sent1_tags = make_tags(sentence1)
    sent2_tags = make_tags(sentence2)

    for v in sent1_tags[::-1]:
        if is_verb(v):
            s1_v = v[0]
            break
        else:
            s1_v = "COMP5211"  # as a filler

    for adj in sent1_tags[::-1]:
        if is_adj(adj):
            s1_j = adj[0]
            break
        else:
            s1_j = "COMP5211"

    for v in sent2_tags[::-1]:
        if is_verb(v):
            s2_v = v[0]
            break
        else:
            s2_v = "COMP5211"

    for adj in sent2_tags[::-1]:
        if is_adj(adj):
            s2_j = adj[0]
            break
        else:
            s2_j = "COMP5211"

    sim_s1_v_s2_v = get_sim_value(s1_v, s2_v)

    sim_s1_j_s2_j = get_sim_value(s1_j, s2_j)

    sim_s1_v_s2_j = get_sim_value(s1_v, s2_j)

    sim_s1_j_s2_v = get_sim_value(s1_j, s2_v)

    sent1_positive = 1
    if is_negative_from_list(sent1_tags):
        sent1_positive = -1

    sent2_positive = 1
    if is_negative_from_list(sent2_tags):
        sent2_positive = -1

    return [sim_s1_v_s2_v, sim_s1_j_s2_j, sim_s1_v_s2_j, sim_s1_j_s2_v, sent1_positive, sent2_positive]


# main + read input data
if __name__ == '__main__':

    print("==== Now, task beginning!!! ====")

    sentences = []
    sent1 = []
    sent2 = []
    conjs = []
    prons = []
    choice0 = []
    choice1 = []
    answer = []

    filepath = "./datasets/WSCollection.xml"

    print("==== Reading XML file: " + os.path.basename(filepath) + " ====")
    print "Start parsering .xml file..."

    xml_data = xml.etree.ElementTree.parse(filepath).getroot()

    size = 0

    for schema in xml_data.findall('schema'):

        # replas = ('.', ''), ('.', ''), ('a', ''), ('an', ''), ('the', '')
        replas = ('.', ''), ('.', ''), ('the', '')

        sent1.append(schema[0][0].text.lower().strip())
        sent2.append(schema[0][2].text.lower().strip())
        prons.append(schema[0][1].text)

        c0 = reduce(lambda a, kv: a.replace(*kv), replas,
                    schema[2][0].text.lower().strip())
        c1 = reduce(lambda a, kv: a.replace(*kv), replas,
                    schema[2][1].text.lower().strip())

        choice0.append(c0)
        choice1.append(c1)

        ans = schema[3].text.strip()
        if ans == 'A':
            answer.append(1)
        else:
            answer.append(-1)

        sentences.append(sent1[size] + ' ' + prons[size] + ' ' + sent2[size])

        size += 1

    print "==== The total number of questions is: ", len(sentences), " ===="
    print "Start training model..."

    total = len(sentences)
    train_size = 200
    train_feature = []
    train_target = answer[:train_size]

    for i in range(train_size):
        s1 = sent1[i]
        s2 = sent2[i]
        feature = extract_feature(s1, s2)
        train_feature.append(feature)

    clf = svm.SVC()
    clf.fit(train_feature, train_target)

    print "Start predictting..."

    test_size = total - train_size
    test_feature = []

    for i in range(test_size):
        s1 = sent1[i + train_size]
        s2 = sent2[i + train_size]
        feature = extract_feature(s1, s2)
        test_feature.append(feature)

    test_answer = clf.predict(test_feature)

    print "Start caculating accuracy..."

    correct = 0
    for i in range(total - train_size):
        if test_answer[i] == answer[i + train_size]:
            correct += 1

    print "Accuracy of SVM/machine learning: ", float(correct) / test_size * 100,  "%"
    print("==== Task finished, this is the last line! ====")
