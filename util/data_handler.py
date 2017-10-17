# -*- coding: utf-8 -*-

import sqlite3

_extendDict = {}
_reduceList = {}


class WordFilter(object):
    isInitialization = False

    def __init__(self):
        if not WordFilter.isInitialization:
            db = sqlite3.connect('db/word_filter.db')

            with db:
                self.createTable(db)

                cursor = db.cursor()
                rv = cursor.execute('select * from extend_words')
                global _extendDict
                _extendDict = {x: y for x, y in rv}

                rv = cursor.execute('select * from extend_words')

                global _reduceList
                _reduceList = [x for x in rv]

                cursor.close()

            WordFilter.isInitialization = True

    def createTable(self, db):
        with open('db/schema/word_filter.sql', encoding='utf-8', mode='r') as f:
            cursor = db.cursor()
            cursor.executescript(f.read())
            db.commit()
            cursor.close()

    def get_extend_word_dict(self):
        return _extendDict

    def add_extend_word(self, match_text, text):
        with sqlite3.connect('db/word_filter.db') as db:
            self.createTable(db)

            cursor = db.cursor()
            rv = cursor.execute('insert or replace into extend_words values(:match_text, :text)',
                                {'match_text': match_text, 'text': text})

            db.commit()
            cursor.close()

            WordFilter.isInitialization = False
            self.__init__()

    def get_reduce_word_list(self):
        return _reduceList

    def add_reduce_word(self, text):
        with sqlite3.connect('db/word_filter.db') as db:
            self.createTable(db)

            cursor = db.cursor()
            rv = cursor.execute('insert or replace into reduce_words values(:text)', {'text': text})

            db.commit()
            cursor.close()

            WordFilter.isInitialization = False
            self.__init__()


class WordRelationship(object):
    def __init__(self):
        pass

    def get_relationship_list(self):
        pass

    def add_relationship(self, source, target, frequency):
        pass


class WordPool(object):
    def __init__(self):
        pass

    def get_word_pool_list(self):
        pass

    def add_word_pool(self, text):
        pass
