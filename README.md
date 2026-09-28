# Mage2Gen Frontend

Django 6.1 / Python 3.14 app that generates Magento 2 modules.

## Local setup with Docker Compose

1. Clone the Mage2Gen cores used by the snippet generator:

```
sh pull_mage2gen_core.sh
```

2. Create local settings from the samples:

```
cp settings/local.py.sample settings/local.py
cp settings/dev.py.sample settings/dev.py
```

`settings/local.py` reads host `127.0.0.1:5433` by default (Postgres published by Compose). Inside the `web` container, Compose sets `MYSQL_HOST=db` and `MYSQL_PORT=5432`.

3. Start Postgres 16, memcached, and the app:

```
docker compose up --build
```

4. Open http://localhost:8000/

Admin is at `/mage_admin/`. Create a superuser from the host venv or with:

```
docker compose exec web python3 manage.py createsuperuser
```

## Local setup with a virtualenv

Requires Python 3.12 or newer (3.14 recommended) and the Compose Postgres service.

```
python3.14 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp settings/local.py.sample settings/local.py
cp settings/dev.py.sample settings/dev.py
docker compose up -d db
python manage.py migrate
python manage.py createcachetable
python manage.py createsuperuser
python manage.py runserver_plus
```

Then open http://localhost:8000/
