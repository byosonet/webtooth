from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'backend': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] => %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': settings.LEVEL_LOG,
            'filters': [],
            'class': 'logging.FileHandler',
            'filename': settings.PATH_LOGS+'/webtooth.log',
            'formatter': 'backend'
        },
        'console': {
            'level': settings.LEVEL_LOG,
            'filters': [],
            'class': 'logging.StreamHandler',
            'formatter': 'backend'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apppatients.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appfiles.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appnavigations.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appimports.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apptasks.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apprecipes.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appproperties.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appadmin.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appinventories.views': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apppatients.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appfiles.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appimports.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apptasks.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apprecipes.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appadmin.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'tasks.config': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.signals': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.decorators': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'django.db.backends': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
         'django.template': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'django.server': {
            'handlers': ['file', 'console'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
    },
}
