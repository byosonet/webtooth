from .base import *

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#Si debug esta en False hay que añadir valores a los HOSTS
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5432'
    }
}

#JOBS LIST FOR WEBTOOTH
JOBLOGMAILTIMER = False
JOBMONITORTIMER = False

##CONFIG LEVEL LOG
LEVEL_LOG = 'INFO'

##PARA HABILITAR REGISTRO DE SITIO
SITE_ID = 1
SITE_DOMAIN = ''
SITE_NAME = 'Webtooth'
