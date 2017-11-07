# -*- coding: utf-8 -*-
from interface.BaseApi import BaseApi
from lexrankr import LexRank

class ThemeSentence(BaseApi):
    # def get(self):
    def post(self):
        import jpype
        if jpype.isJVMStarted():
            jpype.attachThreadToJVM()
        result = []
        corpus = self.params['corpus']

        if corpus:
            result_count = self.params['result_count']
            data_save = self.params['data_save']

            if data_save.upper() == 'Y':
                self.getDataApi().WordPool.add_word_pool(corpus)

            config = {
                # 'useful_tags': ['Noun', 'Verb', 'Adjective', 'Determiner', 'Adverb', 'Conjunction', 'Josa', 'PreEomi',
                #                 'Eomi', 'Suffix', 'Alpha', 'Number'],
                'useful_tags': ['Noun', 'ProperNoun'],
                'min_token_length': 5
            }

            lexRank = LexRank(**config)
            lexRank.summarize(corpus)

            result_count = min(result_count, lexRank.num_sentences-1)
            if result_count == 0:
                result_count = 1

            result = lexRank.probe(result_count)

        return result
