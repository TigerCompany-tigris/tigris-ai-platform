FROM alpine:latest

MAINTAINER Mario Cho <hephaex@gmail.com>

WORKDIR /fasttext

COPY ./fasttext_app.py .

RUN apk add --no-cache --update wget py-pip python-dev musl-dev linux-headers g++ make gfortran ca-certificates \
	&& wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip \
	&& ln -s /usr/include/locale.h /usr/include/xlocale.h \
	&& mkdir -p /tmp/build \
	&& cd /tmp/build \
	&& wget http://www.netlib.org/blas/blas-3.6.0.tgz \
	&& wget http://www.netlib.org/lapack/lapack-3.6.1.tgz \
	&& tar xzf blas-3.6.0.tgz \
	&& tar xzf lapack-3.6.1.tgz \
	&& cd /tmp/build/BLAS-3.6.0/ \
	&& gfortran -O3 -std=legacy -m64 -fno-second-underscore -fPIC -c *.f \
	&& ar r libfblas.a *.o \
	&& ranlib libfblas.a \
	&& mv libfblas.a /tmp/build/. \
	&& cd /tmp/build/lapack-3.6.1/ \
	&& sed -e "s/frecursive/fPIC/g" -e "s/ \.\.\// /g" -e "s/^CBLASLIB/\#CBLASLIB/g" make.inc.example > make.inc \
	&& make lapacklib \
	&& make clean \
	&& mv liblapack.a /tmp/build/. \
	&& cd /fasttext \
	&& export BLAS=/tmp/build/libfblas.a \
	&& export LAPACK=/tmp/build/liblapack.a \
	&& pip --no-cache-dir install --upgrade pip cython \
	&& pip --no-cache-dir install --upgrade flask gensim fasttext spacy \
	&& rm -rf /tmp/build

EXPOSE 5000

CMD ["python", "./fasttext_app.py", "-p", "5000", "-l", "en", "-m", "wiki.en.bin"]
