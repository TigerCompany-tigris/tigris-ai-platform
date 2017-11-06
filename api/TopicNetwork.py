# -*- coding: utf-8 -*-
from interface.BaseApi import BaseApi

class TopicNetwork(BaseApi):
    def get(self):
        dataApi = self.getDataApi()
        keyword = self.params['keyword']
        result_count = self.params['result_count']
        list = dataApi.WordRelationship.get_similar_list(keyword, result_count)


        return list
