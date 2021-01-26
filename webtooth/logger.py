from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] => %(message)s',
            'datefmt': "%d-%m-%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.PATH_LOGS+'/webtooth.log',
            'formatter': 'standard',
            'maxBytes': 1024*1024*1,
            'backupCount': 20,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
        'webtooth.views': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
        'apppatients.views': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
        'appinventories.views': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
        'config': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
        'apppatients.config': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
        'apppatients.signals': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
        'apppatients.decorators': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'standard',
        },
    },
}
