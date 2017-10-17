# -*- coding: utf-8 -*-

from flask_restful import reqparse

from interface.BaseApi import BaseApi


class SearchTopic(BaseApi):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, required=True, help='필수입니다.')
        parser.add_argument('search_line', type=int)
        parser.add_argument('result_count', type=int, default=5)
        args = parser.parse_args()

        text = args['text']

        rtn = {'topics': []}

        if text:
            nwords = int(args['result_count'])
            search_line = args['search_line']

            text_lines = list(filter(lambda l: l, text.splitlines()))

            if search_line:
                text_lines = text_lines[:int(search_line)]

            text_lines = self.cleaning(text_lines)
            rtn['topics'] = self.getTopics(text_lines, nwords)

        return rtn