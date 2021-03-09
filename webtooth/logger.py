from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'backend': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] => %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': settings.LEVEL_LOG,
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': settings.PATH_LOGS+'/webtooth.log',
            'formatter': 'backend'
        },
        'console': {
            'level': settings.LEVEL_LOG,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'backend'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'webtooth.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apppatients.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'appfiles.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'appnavigations.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'appimports.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apptasks.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apprecipes.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'appinventories.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apppatients.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'appfiles.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'appimports.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apptasks.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apprecipes.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'webtooth.signals': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'apppatients.decorators': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': False,
            'formatter': 'backend',
        },
        'django.db.backends': {
            'level': settings.LEVEL_LOG,
            'handlers': ['file', 'console'],
        },
    },
}
