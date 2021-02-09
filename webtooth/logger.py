from django.conf import settings

LEVEL_LOG = 'DEBUG'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'backend': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] => %(message)s',
            'datefmt': "%d-%m-%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': LEVEL_LOG,
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': settings.PATH_LOGS+'/webtooth.log',
            'formatter': 'backend'
        },
        'console': {
            'level': LEVEL_LOG,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'backend'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'webtooth.views': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apppatients.views': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'appinventories.views': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'config': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apppatients.config': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apppatients.signals': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apppatients.decorators': {
            'handlers': ['file', 'console'],
            'level': LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'django.db.backends': {
            'level': LEVEL_LOG,
            'handlers': ['file', 'console'],
        },
    },
}
