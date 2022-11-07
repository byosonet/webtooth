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
        'NAME': 'd8bl7208jsb9h3',
        'USER': 'dfskcnftyzvegj',
        'PASSWORD': '51ee7a0e0137a6ed1f63972afaae2816adaf6f0be32d36d5ed0c40a2a17224c2',
        'HOST': 'ec2-44-194-92-192.compute-1.amazonaws.com',
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
