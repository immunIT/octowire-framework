FROM python:alpine

RUN apk add -U curl wget jq

WORKDIR /opt

RUN curl -s 'https://api.bitbucket.org/2.0/repositories/octowire/octowire-framework/refs/tags?sort=-name&pagelen=1' | jq -r '.values | .[] | .name' | wget 'https://bitbucket.org/octowire/octowire-framework/get/$(cat /dev/stdin).tar.gz' -O octowire-framework.tar.gz

RUN tar xvzf octowire-framework.tar.gz && rm octowire-framework.tar.gz && mv octowire* octowire-framework

WORKDIR octowire-framework

RUN python setup.py install

RUN owfupdate

ENTRYPOINT ["owfconsole"]
