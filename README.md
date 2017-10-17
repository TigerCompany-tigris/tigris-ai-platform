## tigris-ai-platform

### 개요

워드 클라우드, 워드 네트워크, 주제어 추출을 위한 웹서비스 구축을 위한 프로젝트
* 형태소분석기: [konlpy](konlpy.org/ko/latest)
* 분석 알고리즘
  * TopicModel: [gensim - ldamodel](https://radimrehurek.com/gensim/models/ldamodel.html)
  * Word2Vec: [gensim - word2vec](https://radimrehurek.com/gensim/models/word2vec.html)
  * 별도의 내부디비를 이용하여 형태소 분석 결과에서 제거하거나 추가

### 설치 가이드

1. centos
<pre><code>sudo yum install python3, pip</code></pre>
