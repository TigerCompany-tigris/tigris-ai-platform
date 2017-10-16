# -*- coding: utf-8 -*-

from flask_restful import reqparse
from .BaseApi import BaseApi

class SearchTopic(BaseApi):
    @staticmethod
    def url():
        return '/searchTopic'

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, required=True, help='필수입니다.')
        parser.add_argument('search_line', type=int)
        parser.add_argument('result_count', type=int, default=5)
        args = parser.parse_args()

        text = args['text']
        rtn = {'topics': []}

        if not text:
            return rtn

        topics = []
        nwords = int(args['result_count'])
        search_line = args['search_line']

        text_lines = list(filter(lambda l: l, text.splitlines()))

        if not search_line:
            text_lines = text_lines[:int(search_line)]

        text_lines = self.cleaning(text_lines)
        topics = self.getTopics(text_lines, nwords)

        # self.logger.info('topics : %s' % titleTopics)
        # self.logger.info('titleTopics : %s' % titleTopics)
        # self.logger.info('rtn : %s' % rtn)

        return {'topics': topics}