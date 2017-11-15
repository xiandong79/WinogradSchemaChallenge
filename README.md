# 1. COMP5211 Winograd Schema Challenge

Name: Xiandong QI

Student ID: 20403284

Email: xqiad@cse.ust.hk

Date: 2017-11-13

## 1.1. Method-1: Answer by Bing Search Engine

### 1.1.1. Design Philosophy

For sentence "Lions are chasing the sheep because they are predators". We will replace the target pronoun "they" by the correct antecedent and incorrect antecedent, "Lions" and "sheep" for above example separately. We believe that the search engine will pretend to provide more correct information about the "world knowledge".

#### Example in `search_by_Google.py`

```python
sent1 = "Lions are predators"
sent2 = "Sheep are predators"

print google_search(sent1)
print google_search(sent2)
```

The total number of response of above 2 queries are:

```python
<div id="resultStats">約 24,600,000 項搜尋結果<nobr> (0.36 秒) </nobr></div>
<div id="resultStats">約 1,300,000 項搜尋結果<nobr> (0.38 秒) </nobr></div>
```

The algorithm would answer that the pronoun - “they” is "Lions" because that 24,600,000 > 1,300,000 which is intuitively correct. 



### 1.1.2. Why not Google Search Engine?

When using **Google Search Engine** for the total 279 questions, we saw "503 Service Unavailable Error ". This is because Google Search detects the [automated traffic](https://support.google.com/websearch/answer/86640?hl=en) to Google sent by my network. 

So we switched to **Bing search engine** for answering the generated queries in `answer_by_Bing.py` script.



## 1.2. Method-2: Answer by SVM/Machine Learning

### 1.2.1. Introduction of SVM 

A Support Vector Machine (SVM) is a discriminative classifier formally defined by a separating hyperplane. In other words, given labeled training data (supervised learning), the algorithm outputs an optimal hyperplane which categorizes new examples.

In which sense is the hyperplane obtained optimal? Let’s consider the following simple problem:

For a linearly separable set of 2D-points which belong to `one of two classes`, find a separating straight line. (Exactly fit our project, a 2D proplem with Answer A and Answer B)

![](https://docs.opencv.org/2.4/_images/separating-lines.png)


### 1.2.2. Design Philosophy

1. Given each training sentence, we split it into 2 clauses.

2. Find the key word (verb and adjective) of each clause by using nltk.word\_tokenize() and nltk.pos_tag() in make\_tags() function. 

3. Find the similarity of each pair of key word by using wordnet.synsets() and nltk.wup\_similarity() in get\_sim\_value() function. 

4. Find the positve or negative mood of each clause.

5. Return the above 6 features as a feature vector for each sentence.

\# you can learn more concept and features of `nltk` using `test_nltk.py` script.

```python
# part of the "extract_feature" function
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

    sim_s1_v_s2_v = get_sim_value(s1_v, s2_v)

    sent1_positive = 1
    if is_negative_from_list(sent1_tags):
        sent1_positive = -1

    return [sim_s1_v_s2_v, sim_s1_j_s2_j, sim_s1_v_s2_j, sim_s1_j_s2_v, sent1_positive, sent2_positive]
```

### 1.2.3. Evaluation of SVM

```python
# train model
clf = svm.SVC()
clf.fit(train_feature, train_target)

# predict answers
test_answer = clf.predict(test_feature)

```


## 1.3. Implementation （TA，Here!!!）


### 1.3.1. Installation

```bash
$ cd xxx-file-folder  # your workspace
$ git clone https://github.com/xiandong79/WinogradSchemaChallenge.git
$ pip install -U pip
$ pip install -U nltk
$ pip install -r requirements.txt 
```

If you prefer a pure and isolated python environment, 

### 1.3.2. Input data


1. The input data has been ready in `datasets` folder. We mainly use `WSCollection.xml` for our project.

2. File-path of `WSCollection.xml` has been fixed in two scripts for connivence.


### 1.3.3. Run Code

#### Method-1: Answer by Bing Search Engine

##### Execution:

```bash
$ cd WinogradSchemaChallenge
$ python2 answer_by_Bing.py

```
##### Result:

```bash
==== The total number of questions is:  279  ====
Accuracy of Bing Search Engine:  51.61 %
```


#### Method-2: Answer by SVM/Machine Learning

##### Execution:

```bash
$ python2 answer_by_machine_learning.py

```

##### Result:

```bash
==== The total number of questions is:  279  ====
Accuracy of SVM/machine learning:  53.16 %
```


## 1.4. Rethinking

### 1.4.1. Drawback of Search Engine

The Google/Bing search engine may return some unexpected results for our question. For example, "The police is chasing an accountant because he is a bad guy". In search engine filled with news, it will answer "police is the bad guy" which is not the correct answer for our question.


## 1.5. Future Work
The pain spot of Winograd Schema Challenge is that it does not have large amount training data which can be utilized as the common-sense knowledge like human have. It is possible to incorporate various common-sense knowledge bases, including ConceptNet, WordNet, Stanford NLP as the knowledge base in training process. 

## 1.6. Reference

[1] Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning, pp. 777-789, 2012.

[2] http://www.google.de/search?

[3] http://www.bing.com/search

[4] http://www.nltk.org

[5] http://scikit-learn.org/stable/modules/svm.html

[6] https://docs.opencv.org/2.4/doc/tutorials/ml/introduction_to_svm/introduction_to_svm.html


