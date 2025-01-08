"""Base settings shared by all environments"""

import os
import sys

from settings import local

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
MODULE_GENERATION_PATH = False

# create tmp dir if not exists
try:
    os.makedirs(TMP_DIR)
except Exception:
    pass

#==============================================================================
# Generic Django project settings
#==============================================================================

#TODO remove * when live
ALLOWED_HOSTS = ['*', 'mage2gen.com']

TIME_ZONE = 'Europe/Amsterdam'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en-en'

SECRET_KEY = local.SECRET_KEY

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'social_django',
    'compressor',

    'apps.mage2gen.apps.Mage2GenConfig',
    'apps.account.apps.AccountConfig',
    'rest_framework'
)

#==============================================================================
# Project URLS and media settings
#==============================================================================
ROOT_URLCONF = 'urls'

LOGIN_URL = 'accounts:login'
LOGOUT_URL = 'accounts:logout'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = 'wsgi.application'

#==============================================================================
# Middleware
#==============================================================================
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'
)

#==============================================================================
# Auth / security
#==============================================================================

GRAPPELLI_ADMIN_TITLE = 'Mage2Gen'

#Google login
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '237264176477-2dhiodmebpnoieekrrbfjiagb828eqvl.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'QInrQrrvpAFV2rGQo6WSm6sD'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

#==============================================================================
# Template settings
#==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',

                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'apps.mage2gen.context_processors.add_snippets',
                'django.template.context_processors.request',
            ],
            'loaders': (
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ),
        }
    },
]


#==============================================================================
# Cache backend
#==============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',
    }
}

#==============================================================================
# database
#==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': local.MYSQL_DB,
        'USER': local.MYSQL_USERNAME,
        'PASSWORD': local.MYSQL_PASSWORD,
        'HOST': local.MYSQL_HOST,
        'PORT': local.MYSQL_PORT,
    }
}

#==============================================================================
# Composser 
#==============================================================================

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']
