# -*- coding: utf-8 -*-
import abc

class AbsWordPool():
    """
    유사어 추출등에서 사용할 데이터 Abstract Class
    """
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_word_pool_list(self, params=None):
        """
        데이터(문장) 세트 반환
        :return: [words, ...]
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def add_word_pool(self, text, params=None):
        """
        데이터(문장) 저장
        :param text: 추가할 데이터(문장)
        :return: None
        """
        raise NotImplementedError()


class AbsWordFilter():
    """
    데이터(문장)에서 별도의 단어 처리 Abstract Class
    """
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_extend_word_dict(self, params=None) -> dict:
        """
        확장 처리할 단어세트 반환
        :return: {match_key: result_key, ...}
        """
        raise NotImplementedError()

    def add_extend_word(self, match_text, text, params=None):
        """
        확장 처리 단어 추가
        :param match_text: 문장과 비교할 단어
        :param text: 반환할 단어
        :return: None
        """
        pass

    @abc.abstractmethod
    def get_reduce_word_list(self, params=None) -> list:
        """
        문장내에서 제거할 단어세트
        :return: [text, ...]
        """
        raise NotImplementedError()

    def add_reduce_word(self, text: str, params=None):
        """
        제거할 단어 추가
        :param params:
        :param text: 단어
        :return: None
        """
        pass


class AbsWordRelationship():
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_similar_list(self, keyword, result_count, params=None):
        raise NotImplementedError()


class DataApi(object):
    """
    API 서비스에서 사용할 데이터 Class
    """
    __wordFilter = None  # type: AbsWordFilter
    __wordPool = None  # type: AbsWordPool
    __wordRelationship = None  # type: AbsWordRelationship

    @property
    def WordFilter(self) -> AbsWordFilter:
        return DataApi.__wordFilter

    @WordFilter.setter
    def WordFilter(self, cls: AbsWordFilter):
        DataApi.__wordFilter = cls()

    @property
    def WordPool(self) -> AbsWordPool:
        return DataApi.__wordPool

    @WordPool.setter
    def WordPool(self, cls: AbsWordPool):
        obj = cls()
        DataApi.__wordPool = obj

    @property
    def WordRelationship(self) -> AbsWordRelationship:
        return DataApi.__wordRelationship

    @WordRelationship.setter
    def WordRelationship(self, cls: AbsWordRelationship):
        DataApi.__wordRelationship = cls()