# -*- coding: utf-8 -*-
from interface.BaseApi import BaseApi

class SearchTopic(BaseApi):
    def post(self):
        text = self.params['text']
        rtn = {'topics': []}

        if text:
            result_count = int(self.params['result_count'])
            search_line = self.params['search_line']
            data_save = self.params['data_save']

            if data_save.upper() == 'Y':
                self.getDataApi().WordPool.add_word_pool(text)

            text_lines = list(filter(lambda l: l, text.splitlines()))

            if search_line:
                text_lines = text_lines[:int(search_line)]

            text_lines = BaseApi.cleaning(text_lines, self.params)
            rtn['topics'] = BaseApi.getTopics(text_lines, result_count, self.params)

        return rtn