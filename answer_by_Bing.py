##############################################################
#####       Answer by Bing Search Engine                 #####
#####       Author: Xiandong QI                          #####
#####       Time: 2017-11-12                             #####
##############################################################

import re
import os
import contextlib
from urllib2 import Request, urlopen
import urllib
import xml.etree.ElementTree
from bs4 import BeautifulSoup


def bing_search(sentence):

    url = "http://www.bing.com/search?q=%s" % urllib.quote_plus(sentence)
    reponse = Request(url)
    reponse.add_header(
        'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')
    bing_response = urlopen(reponse).read()

    soup = BeautifulSoup(bing_response, 'html.parser')
    count = soup.find('div', id='b_tween').text
    contextlib.closing(bing_response)

    return int(re.sub("[^0-9]", "", count))


def bing_answer():
    corrected = 0
    answerbybing = []

    for i in range(size):  # size = 279
        question0 = choice0[i] + " " + sent2[i]
        count0 = bing_search(question0)
        # print question0
        # print count0
        question1 = choice1[i] + " " + sent2[i]
        count1 = bing_search(question1)
        # print question1
        # print count1

        if count0 > count1:
            # print choice0[i]
            answerbybing.append(choice0[i])
        else:
            # print choice1[i]
            answerbybing.append(choice1[i])

    for j in range(size):
        print "Answer by Bing: ", answerbybing[j], "Correct Answer: ", answer[j]
        if answerbybing[j] == answer[j]:
            corrected += 1

    return corrected


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
            answer.append(c0)
        else:
            answer.append(c1)

        sentences.append(sent1[size] + ' ' + prons[size] + ' ' + sent2[size])

        size += 1

        # if size == 70:
        #     print sentences[70]
    # print size
    # print len(choice0)
    # print choice0[70]
    # print len(answer)
    print "The total number of questions is: ", len(sentences)

    accuracy = float(bing_answer()) / size * 100

    print "Accuracy of Answered by Bing Search Engine: ", accuracy, "%"
    print("==== Task finished, this is the last line! ====")
