# -*-coding: utf-8 -*-
import multiprocessing

from gensim.models import Word2Vec

def run_word2vec(file_path, sentences, config=None):
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

    model = Word2Vec(sentences, **config)
    model.init_sims(replace=True)
    model.save(file_path)
    return model


if __name__ == '__main__':
    sentences = []

    run_word2vec('db/word2vec.model', sentences)

    pass