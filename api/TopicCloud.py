# -*- coding: utf-8 -*-
from interface.BaseApi import BaseApi

class TopicCloud(BaseApi):
    def get(self):
        dataApi = BaseApi.getDataApi()
        dataList = dataApi.WordPool.get_word_pool_list(self.params)
        result_count = self.params['result_count']

        tags = []

        for data in dataList:
            lines = list(filter(lambda l: l, data.splitlines()))
            lines = BaseApi.cleaning(lines, self.params)

            topics = BaseApi.getTopics(lines, result_count, self.params)

            if topics:
                tags.extend(topics)

        rtn = BaseApi.getTags(tags, result_count, self.params)

        return rtn