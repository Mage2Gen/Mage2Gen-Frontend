import os

DEBUG = bool(int(os.getenv('DJANGO_IS_DEBUG', True)))

if DEBUG:
	from .dev import *
else:
	from .live import *

#Overule import DEBUG with env DEBUG
DEBUG = bool(int(os.getenv('DJANGO_IS_DEBUG', True)))
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG