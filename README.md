## tigris-ai-platform

### 개요

워드 클라우드, 워드 네트워크, 주제어 추출을 위한 웹서비스 구축을 위한 프로젝트
* 형태소분석기: [konlpy](konlpy.org/ko/latest)
* 분석 알고리즘
  * TopicModel: [gensim - ldamodel](https://radimrehurek.com/gensim/models/ldamodel.html)
  * Word2Vec: [gensim - word2vec](https://radimrehurek.com/gensim/models/word2vec.html)
  * 별도의 내부디비를 이용하여 형태소 분석 결과에서 제거하거나 추가

### 설치 가이드
Install Java 1.7 or up
1. python3 설치
  * ubuntu or linux
      <pre><code>sudo apt-get install g++ openjdk-8-jdk python3-dev</code></pre>
  * centos
    <pre><code>sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
    sudo yum install gcc-c++ java-1.8.0-openjdk-devel.x86_64 python36u python36u-libs python36u-devel python36u-pip</code></pre>

2. 필수 패키지 설치
* 가상화 처리시
<pre><code>설치 : python3 -m venv {가상환경명}
사용 : source {가상환경명}/bin/activate
</code></pre>
<pre><code>pip3 install cython, jpype1, sklearn, scipy, gensim, flask_restful, konlpy
가상환경에서 설치시: pip install cython, jpype1, sklearn, scipy, gensim, flask_restful, konlpy
</code></pre>

3. 프로젝트 다운로드
```bash
git clone https://github.com/TigerCompany-tigris/tigris-ai-platform.git
```
4. 사용 가이드
* 환경설정
* 서버 구동
```bash
```
* API 호출
  
