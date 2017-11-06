# -*- coding: utf-8 -*-
from __future__ import absolute_import

import multiprocessing
import os

from util.nlp import nlp_twitter
from util.data_handler import WordPool

from gensim.models import Word2Vec
from interface import BaseApi


def run_model(file_path, config=None, sentences=None):
    if not config:
        config = {
            'min_count': 3,  # 등장 횟수가 5 이하인 단어는 무시
            'size': 300,  # 300차원짜리 벡터스페이스에 embedding
            'sg': 0,  # 0이면 CBOW, 1이면 skip-gram을 사용한다
            'hs': 1,
            'batch_words': 10000,  # 사전을 구축할때 한번에 읽을 단어 수
            'iter': 10,  # 보통 딥러닝에서 말하는 epoch과 비슷한, 반복 횟수
            'workers': multiprocessing.cpu_count(),
            'compute_loss': True
        }

    if not sentences:
        sentences = []
        pool_list = WordPool().get_word_pool_list({'data_count': 20})

        for data in pool_list:
            lines = list(filter(lambda l: l, data.splitlines()))
            lines = BaseApi.cleaning(lines)
            sentences += [nlp_twitter(line) for line in lines if line]

    model = Word2Vec(sentences, **config)
    model.init_sims(replace=True)
    model.save(file_path)
    return model

def get_model(model_file):
    if not os.path.isfile(model_file):
        model = run_model(model_file)
        return model

    model = Word2Vec.load(model_file)
    model.init_sims(replace=True)

    return model


if __name__ == '__main__':
    print('main')
    # run_model('db/word2vec.model')