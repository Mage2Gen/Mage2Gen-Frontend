#!/bin/sh
set -e
cd /usr/src/app

python3 manage.py migrate --noinput
python3 manage.py createcachetable
python3 manage.py runserver_plus '0.0.0.0:8000'
