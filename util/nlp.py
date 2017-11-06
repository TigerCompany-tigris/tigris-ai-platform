# -*- coding: utf-8 -*-
def nlp_twitter(text):
    import jpype
    if jpype.isJVMStarted():
        jpype.attachThreadToJVM()

    from konlpy.tag import Twitter
    return [n[0] for n in Twitter().pos(text, norm=False, stem=True) if n[1] in ('Noun', 'ProperNoun')]