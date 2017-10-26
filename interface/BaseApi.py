# -*- coding: utf-8 -*-
import copy
import numpy as np, re
import re
from collections import Counter
from functools import wraps
from itertools import chain

from flask import request
from flask_restful import Resource, reqparse
from gensim import corpora, models

from .DataApi import DataApi

nlp = None
dataApi = None  # type: DataApi


def cleaning(content_list, params=None):
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
        contents = ' '.join([word for word in word_tokenize(contents, language='english') if
                             word.lower() not in set(stopwords.words('english'))])
        rtn.append(contents)

    return rtn


def getTags(tags, result_count, params=None):
    if not tags:
        return []

    count = Counter(tags)
    count_most = count.most_common(result_count)

    rtn = {'min': min(count_most, key=lambda k: k[1])[1],
           'max': max(count_most, key=lambda k: k[1])[1],
           'data': [{'text': n, 'frequency': c} for n, c in count_most]}

    return rtn


def getTopics(text_lines, nwords, params=None):
    rtnList = []

    for data in text_lines:
        for d in data.split():
            for match_text, text in dataApi.WordFilter.get_extend_word_dict(params).items():
                if len(rtnList) == nwords:
                    return rtnList

                if d.lower() == match_text.lower():
                    isContinue = False
                    for rtn in rtnList:
                        if text in rtn:
                            isContinue = True
                            break

                    if not isContinue:
                        rtnList.append(text)

    if len(rtnList) == nwords:
        return rtnList

    def tag_generator(corpus):
        for data in corpus:
            yield [p for p in nlp(data) if len(p) > 1 and p not in dataApi.WordFilter.get_reduce_word_list(params)]

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
                    newDict[key] += (idx + 1 + value)
                else:
                    newDict[key] = (idx + 1 + value)
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


def decorators(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        if kwargs:
            f.__self__.params.update(kwargs)
        return f(*args)
    return func_wrapper

class BaseApi(Resource):
    method_decorators = [decorators]

    __default_params = {
        'name': '',
        'dest': '',
        'default': '',
        'type': str,
        'required': False,
        'action': 'store',
        'help': ''
    }

    def __init__(self, parameters):
        if request.method in parameters:
            paramList = parameters[request.method]

            def param_parser(default, param):
                default.update({k: v for k, v in param.items() if v})
                default['type'] = eval(default['type'])
                default['required'] = bool(default['required'])
                default['default'] = default['type'](default['default'])

                return default

            parser = reqparse.RequestParser()

            for param in paramList:
                parser.add_argument(**param_parser(BaseApi.__default_params.copy(), param))

            self.params = parser.parse_args()

    @staticmethod
    def cleaning(content_list, params=None):
        return cleaning(content_list, params)

    @staticmethod
    def getTags(tags, result_count, params=None):
        return getTags(tags, result_count, params)

    @staticmethod
    def getTopics(text_lines, nwords, params=None):
        return getTopics(text_lines, nwords, params)

    @staticmethod
    def getDataApi():
        return dataApi