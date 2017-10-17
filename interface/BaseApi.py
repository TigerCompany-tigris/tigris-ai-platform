# -*- coding: utf-8 -*-
from flask_restful import Resource
from collections import Counter
from gensim import corpora, models
from itertools import chain

import numpy as np
import re

_nlp = None

word_pool = None
word_filter = None
word_relationship = None

def get_nlp():
    return nlp
def set_nlp(v):
    global nlp
    nlp = v

def cleaning(content_list):
    rtn = []
    for contents in content_list:
        # html 제거
        contents = re.sub(r'<.+?>', '', contents, 0, re.I | re.S)
        # 마그넷주소 제거
        contents = re.sub(r'magnet:.*(\w)+', '', contents, 0, re.I | re.S)
        # 이메일 제거
        contents = re.sub(r'[\w.-]+@[\w.-]+.\w+', '', contents, 0, re.I | re.S)
        # URL 제거
        contents = re.sub(
            r'(((file|gopher|news|nntp|telnet|https?|ftps?|sftp)\:(\/\/)?)?)([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?',
            '', contents, 0, re.I | re.S)

        # 특수문자 제거
        contents = re.sub(r'(\W|_)', ' ', contents, 0, re.I | re.S)

        # 영문 조사등 제거
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        contents = ' '.join([word for word in word_tokenize(contents, language='english') if word.lower() not in set(stopwords.words('english'))])
        rtn.append(contents)

    return rtn

def getTags(tags, result_count):
    if not tags:
        return []

    count = Counter(tags)
    count_most = count.most_common(result_count)

    rtn = {'min': min(count_most, key=lambda k: k[1])[1],
           'max': max(count_most, key=lambda k: k[1])[1],
           'data': [{'text': n, 'frequency': c} for n, c in count_most]}

    return rtn

def getTopics(text_lines, nwords):
    rtnList = []

    for data in text_lines:
        for d in data.split():
            for match_text, text in word_pool.get_extend_word_dict():
                if len(rtnList) == nwords:
                    return rtnList

                if d.lower() == tag.lower():
                    isContinue = False
                    for rtn in rtnList:
                        if real_tag in rtn:
                            isContinue = True
                            break

                    if not isContinue:
                        rtnList.append(real_tag)

    if len(rtnList) == nwords:
        return rtnList

    def tag_generator(corpus):
        for data in corpus:
            yield [p for p in nlp(data) if len(p) > 1 and p not in word_pool.get_reduce_word_list()]

    tagList = [x for x in tag_generator(text_lines) if x]
    tagList = [list(filter(lambda tag: tag not in rtnList, tags)) for tags in tagList]

    if not tagList or not list(chain.from_iterable(tagList)):
        return rtnList

    dictionary_ko = corpora.Dictionary(tagList)

    tf_ko = [dictionary_ko.doc2bow(text) for text in tagList]
    tfidf_model_ko = models.TfidfModel(tf_ko)
    tfidf_ko = tfidf_model_ko[tf_ko]

    np.random.seed(42)
    ntopics = len(text_lines)
    lda_ko = models.ldamodel.LdaModel(tfidf_ko, id2word=dictionary_ko, num_topics=ntopics, passes=1)
    topics = lda_ko.show_topics(num_topics=ntopics, num_words=5, formatted=False)

    def sumTopic(topics):
        newDict = {}

        for topic in topics:
            topic[1].reverse()
            for idx, obj in enumerate(topic[1]):
                key, value = obj
                if key in newDict:
                    newDict[key] += (idx+1+value)
                else:
                    newDict[key] = (idx+1+value)
        return newDict

    rtn = sumTopic(topics)
    rtn = [r[0] for r in sorted(rtn.items(), key=lambda d: d[1], reverse=True)]

    for r in rtn:
        if len(rtnList) == nwords:
            return rtnList
        hasTopic = False

        for topic in rtnList:
            if r in topic:
                hasTopic = True
                break

        if not hasTopic:
            rtnList.append(r)

    return rtnList

class BaseApi(Resource):
    def cleaning(self, content_list):
        return cleaning(content_list)

    def getTags(self, tags, result_count=20):
        return getTags(tags, result_count)

    def getTopics(self, text_lines, nwords):
        return getTopics(text_lines, nwords)