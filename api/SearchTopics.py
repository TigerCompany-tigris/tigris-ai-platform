# -*- coding: utf-8 -*-

from flask_restful import reqparse

from interface.BaseApi import BaseApi


class SearchTopic(BaseApi):
    def get(self):
        text = self.params['text']
        rtn = {'topics': []}

        if text:
            result_count = int(self.params['result_count'])
            search_line = self.params['search_line']

            text_lines = list(filter(lambda l: l, text.splitlines()))

            if search_line:
                text_lines = text_lines[:int(search_line)]

            text_lines = BaseApi.cleaning(text_lines, self.params)
            rtn['topics'] = BaseApi.getTopics(text_lines, result_count, self.params)

        return rtn