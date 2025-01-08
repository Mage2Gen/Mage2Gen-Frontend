###Installing requirements on Debian/Ubuntu

	sudo apt-get install python3-pip python-virtualenv
    sudo apt-get install pip

##**Project Setup**

**Create virtualenv**
Navigate to the root of the project folder. Run the following command:

    virtualenv --python=/usr/bin/python3 env

**Activate virtualenv**

    . env/bin/activate
    
**Install requirements with pip**

    pip install -r requirements.txt

**create settings/local.py*
```
MYSQL_DB = ''
MYSQL_USERNAME = ''
MYSQL_PASSWORD = ''
MYSQL_HOST = ''
MYSQL_PORT = ''

SECRET_KEY = 'sdafdsfas'
USE_SQLITE = 1
MODULE_GENERATION_PATH = 'path to magento app/code'
```

**Create database tables by running this command:**
if error then comment line 21

	python manage.py migrate

**Caching setup**
Default cache backend settings is the database, for creating the cache table run the following command

	python manage.py createcachetable

**Admin account**
Create user account with admin right for accessing the admin panel:

	python manage.py createsuperuser

##**Running local**

0) Navigate in the project root

1) Activate local environment 

   . ../env/bin/activate
    
2) Starting the webserver:
    
    python manage.py runserver_plus
    
3) Open the browser and navigate to http://localhost:8000/



node-sass scss/ --output css


##**Running and developing with docker**

```
sh pull_mage2gen_core.sh
```

```
docker build -t mage2gen .
```

```
cp settings/dev.py.sample settings/dev.py
cp settings/local.py.sample settings/local.py
```

```
docker run -it --rm --name mage2gen -p 8000:8000 -v $(pwd):/usr/app/src mage2gen
```
