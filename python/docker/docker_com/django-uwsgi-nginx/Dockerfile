FROM ubuntu:16.04

MAINTAINER Dockerfiles

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        git \
        python3 \
        python3-dev \
        python3-setuptools \
        python3-pip \
        nginx \
        vim \
        supervisor \
        libmysqlclient-dev && \
        rm -rf /var/lib/apt/lists/*

RUN pip3 install -i https://pypi.doubanio.com/simple/ --upgrade pip
RUN pip3 install -i https://pypi.doubanio.com/simple/ uwsgi
ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8
COPY com/r.txt requirment.txt
RUN mkdir /code
COPY com /code/
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisor-app.conf /etc/supervisor/conf.d/

RUN pip3 install -i https://pypi.doubanio.com/simple/ -r requirment.txt
ENV MYSQL_DATABASE_NAME guo
ENV EMAIL_HOST_USER xing.ms@outlook.com
ENV EMAIL_HOST_PASSWORD 123xing.0


EXPOSE 80

#CMD ['supervisord','-n']
