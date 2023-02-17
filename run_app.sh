#!/bin/sh
cd /usr/app/src

python3 manage.py migrate --noinput
python3 manage.py createcachetable
python3 manage.py runserver_plus '0.0.0.0:8000'
