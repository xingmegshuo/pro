#!/bin/bash

if ! sudo docker images |grep com;then
    sudo docker build -t com django-uwsgi-nginx
fi


if sudo docker ps -a |grep -i comapp; then
    sudo docker rm -f comapp
    sudo docker run -itd --link mysql:mysql --name comapp -p 80:80 \
        com
else
    sudo docker run -itd --link mysql:mysql -p 80:80 \
        com \
        sh -c 'python3 code/com/manage.py migrate && supervisord -n'
fi
