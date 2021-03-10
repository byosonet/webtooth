"""
Django settings for webtooth project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ee@#=1ivnkbyqflvaj#l=fn02xcec@eu6(_=v6%lcpinchwqee'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#Si debug esta en False hay que añadir valores a los HOSTS
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apppatients',
    'appinventories',
    'appfiles',
    'appnavigations',
    'appimports',
    'apptasks',
    'apprecipes',
    'appproperties',
    'appadmin',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'webtooth.middleware.RequestMiddleware'
]

ROOT_URLCONF = 'webtooth.urls'

#Indicando el path del proyecto:
projectPath=BASE_DIR+"/webtooth/"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [projectPath+'templates',projectPath+'css'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'webtooth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER':'postgres',
        'PASSWORD':'root',
        'HOST':'127.0.0.1',
        'DATABASE_PORT':'5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-eu'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DECIMAL_SEPARATOR = '.'
DATE_FORMAT = 'l d/F/Y'
DATETIME_FORMAT='d/b/y H:i a'

DATE_INPUT_FORMAT = ('%d/%m/%Y', '%Y-%m-%d')
DATE_INPUT_SHOW = '%d/%m/%Y'

DATETIME_INPUT_FORMAT = ('%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M')
DATETIME_INPUT_SHOW = '%d/%m/%Y %H:%M'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

#Directory allow media files
MEDIA_URL = '/media/'
MEDIA_ROOT = projectPath+'media'
MEDIA_PATH = projectPath+'media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(projectPath, 'staticprod')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [projectPath+'static']
PATH_LOGS = projectPath+'logs'
PATH_ZIPMAIL = projectPath+'zipmail/'

#DATOS PARA ENVIO DE EMAIL DESDE CTA DE GMAIL
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER="noreply.webtooth@gmail.com"
EMAIL_HOST_PASSWORD="fxqhjfqtammvdndu"

EMAIL_HOST_SUPPORT=["gtrejo.armenta@gmail.com"]
#VARIABLES GLOBALES
EMAIL_TO = []
EMAIL_CC = []
EMAIL_BCC = ["gtrejo.armenta@gmail.com"]

#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIE_AGE = 10  #5min
#SESSION_SAVE_EVERY_REQUEST = True
MAX_TIME_MINUTES_SESSION = 3
SESSION_EXPIRY_SECONDS = 300

MESSAGE_TAGS = {
    messages.DEBUG: 'bg-',
    messages.INFO: 'bg-',
    messages.SUCCESS: 'bg-',
    messages.WARNING: 'bg-',
    messages.ERROR: 'bg-',
 }

#JOBS LIST FOR WEBTOOTH
JOBLOGMAILTIMER = True
JOBMONITORTIMER = False

#MAX RESULT QUERY
MAX_ROWS_QUERY_MODEL = 999999
MAX_ROWS_QUERY_MODEL_NAVIGATION = 1000

##CONFIG CROSS ORIGIN
CORS_ORIGIN_ALLOW_ALL = True

##CONFIG LEVEL LOG
LEVEL_LOG = 'INFO'
PROPAGATE_LOG = True