# -*- coding: utf-8 -*-

from konlpy.tag import Twitter

def nlp_twitter(text):
    return [n[0] for n in Twitter().pos(text, norm=False, stem=True) if n[1] in ('Noun', 'ProperNoun')]