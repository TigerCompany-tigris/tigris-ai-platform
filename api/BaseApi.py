# -*- coding: utf-8 -*-
import abc
import re
from flask_restful import Resource
from collections import Counter
from itertools import chain
from flask import g
from gensim import corpora
from gensim import models
import numpy as np

def feed_cleaning(content_list):
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

def get_tags(tags, result_count):
    if not tags:
        return []

    count = Counter(tags)
    count_most = count.most_common(result_count)

    rtn = {'min': min(count_most, key=lambda k: k[1])[1],
           'max': max(count_most, key=lambda k: k[1])[1],
           'data': [{'text': n, 'frequency': c} for n, c in count_most]}

    return rtn

def get_topics(corpus, nwords, nlp, extends_nlp, reduces_nlp):
    rtnList = []

    for data in corpus:
        for d in data.split():
            for extends in extends_nlp:
                tag, real_tag = extends['text'], extends['real_text']
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

    def tag_generator(nlp, corpus):
        for data in corpus:
            yield [p[0] for p in nlp.pos(data, stem=True, norm=False) if
                   p[1] in ('Noun', 'ProperNoun') and len(p[0]) > 1 and p[0] not in reduces_nlp]

    tagList = [x for x in tag_generator(nlp, corpus) if x]
    tagList = [list(filter(lambda tag: tag not in rtnList, tags)) for tags in tagList]

    if not tagList or not list(chain.from_iterable(tagList)):
        return rtnList

    dictionary_ko = corpora.Dictionary(tagList)

    tf_ko = [dictionary_ko.doc2bow(text) for text in tagList]
    tfidf_model_ko = models.TfidfModel(tf_ko)
    tfidf_ko = tfidf_model_ko[tf_ko]

    np.random.seed(42)  # optional
    ntopics = len(corpus)
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
    def __init__(self, g_db, extends_nlp, reduces_nlp):
        self._db = g_db
        self.logger = g.logger
        from konlpy.tag import Twitter
        self._nlp = Twitter()
        self._extends_nlp = extends_nlp
        self._reduces_nlp = reduces_nlp

    @staticmethod
    @abc.abstractmethod
    def url():
        raise NotImplementedError()

    @property
    def db(self):
        return self._db

    @db.getter
    def get_db(self):
        return self._db

    def feed_cleaning(self, content_list):
        return feed_cleaning(content_list)

    def get_tags(self, tags, result_count=20):
        return get_tags(tags, result_count)

    def get_topics(self, corpus, nwords):
        return get_topics(corpus, nwords, self._nlp, self._extends_nlp, self._reduces_nlp)