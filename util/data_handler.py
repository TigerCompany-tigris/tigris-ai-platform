# -*- coding: utf-8 -*-

import sqlite3
import os
from interface import DataApi

class WordFilter(DataApi.AbsWordFilter):
    __dataFile = 'db/word_filter.db'
    __schemaFile = 'db/schema/word_filter.sql'

    __extendDict = {}
    __reduceList = []

    def __init__(self):
        db = sqlite3.connect(WordFilter.__dataFile)

        with db:
            WordFilter.__createTable(db)
            cursor = db.cursor()

            rv = cursor.execute('select * from extend_words')
            WordFilter.__extendDict = {x: y for x, y in rv}

            rv = cursor.execute('select text from reduce_words')
            WordFilter.__reduceList = [x[0] for x in rv]

            cursor.close()

    def get_extend_word_dict(self, params=None):
        return WordFilter.__extendDict

    def get_reduce_word_list(self, params=None):
        return WordFilter.__reduceList

    def add_extend_word(self, match_text, text, params=None):
        with sqlite3.connect(WordFilter.__dataFile) as db:
            WordFilter.__createTable(db)

            cursor = db.cursor()
            cursor.execute('insert or replace into extend_words values(:match_text, :text)',
                                {'match_text': match_text, 'text': text})

            db.commit()
            cursor.close()

            self.__init__()

    def add_reduce_word(self, text, params=None):
        with sqlite3.connect(WordFilter.__dataFile) as db:
            WordFilter.__createTable(db)

            cursor = db.cursor()
            cursor.execute('insert or replace into reduce_words values(:text)', {'text': text})

            db.commit()
            cursor.close()

            self.__init__()

    @classmethod
    def __createTable(cls, db):
        with open(cls.__schemaFile, encoding='utf-8', mode='r') as f:
            cursor = db.cursor()
            cursor.executescript(f.read())
            db.commit()
            cursor.close()


class WordRelationship(DataApi.AbsWordRelationship):
    __model_file = 'db/word2vec.model'
    __model = None

    def __init__(self):
        from model import word2vec as wv
        WordRelationship.__model = wv.get_model(WordRelationship.__model_file)

    def get_similar_list(self, keyword, result_count, params=None):
        results = WordRelationship.__model.most_similar(keyword, topn=result_count)

        results = [{'keyword': result[0], 'frequency': result[1]} for result in results]
        return sorted(results, key=lambda x: x['frequency'], reverse=True)


class WordPool(DataApi.AbsWordPool):
    __data_path = 'db/pool'
    __data_set = []

    def __init__(self):
        file_list = list(filter(lambda f: os.path.isfile(os.path.join(WordPool.__data_path, f)),
                                os.listdir(WordPool.__data_path)))

        WordPool.__data_set = []
        for file in file_list:
            with open(os.path.join(WordPool.__data_path, file), mode='r', encoding='utf-8') as f:
                WordPool.__data_set.append(f.read())

    def get_word_pool_list(self, params=None):
        if params and 'data_count' in params and params['data_count']:
            return WordPool.__data_set[:params['data_count']]

        return WordPool.__data_set

    def add_word_pool(self, text, params=None):
        WordPool.__data_set.append(text)

        import uuid
        filename = str(uuid.uuid4()) + '.txt'
        with open(os.path.join(WordPool.__data_path, filename), mode='w', encoding='utf-8') as f:
            f.write(text)