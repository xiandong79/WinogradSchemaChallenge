import requests
import re
import os
import sys                                                                                                                                                                  
from urllib2 import Request, urlopen                                                                                                                                        
import urllib                                                                                                                                                               
from bs4 import BeautifulSoup   
import logging
import json
import xml.etree.ElementTree

#for input processing
import xmltodict
import itertools
from bs4 import BeautifulSoup
import re
import time

#for stanford parser
from pycorenlp import StanfordCoreNLP
import nltk
from nltk.stem.wordnet import WordNetLemmatizer


def load_narrative_chain():
    with open('datasets/chain.txt') as f:
        lines = f.readlines()
    chains = []
    for i in range(0,len(lines)):
        if '[' in lines[i]:
            chains.append(lines[i])

    for i in range(0, len(chains)):
        pos = chains[i].find(']')
        chains[i] = chains[i][:pos] + ']'
    return chains


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
    # flags = []

    filepath = "./datasets/WSCollection.xml"

    print("==== reading XML file: " + os.path.basename(filepath) + " ====")

    xml_data = xml.etree.ElementTree.parse(filepath).getroot()

    size = 0

    for schema in xml_data.findall('schema'):
        
        replas = ('.', ''), ('.', ''), ('a', ''), ('an', ''), ('the', '')

        sent1.append(schema[0][0].text.lower().strip())
        sent2.append(schema[0][2].text.lower().strip())
        prons.append(schema[0][1].text)

        c0=reduce(lambda a, kv: a.replace(*kv), replas, schema[2][0].text.lower().strip())
        c1=reduce(lambda a, kv: a.replace(*kv), replas, schema[2][1].text.lower().strip())

        choice0.append(c0)
        choice1.append(c1)

        ans = schema[3].text.strip()
        if ans == 'A':
            answer.append(c0)
        else:
            answer.append(c1)   

        sentences.append(sent1[size] + ' ' + prons[size] + ' ' + sent2[size])

        size += 1

    print "The total number of queations is: ", size
    print "The total number of queations is: ", len(sentences)


    narrative_chain = load_narrative_chain()

    print narrative_chain[0]
    print narrative_chain[1]
    print narrative_chain[2]
    print narrative_chain[0:5]
    print len(narrative_chain)

    print("==== Task finished, this is the last line! ====")