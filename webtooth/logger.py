from django.conf import settings

def filter_record_error(record):
    if record.levelname == settings.FILTER_FILE_ERROR or settings.FLAG_ERROR:
        settings.FLAG_ERROR = True
        if settings.FLAG_COUNT > 0:
            settings.FLAG_COUNT = settings.FLAG_COUNT - 1
            return True
        else:
            settings.FLAG_COUNT = 6
            settings.FLAG_ERROR = False
            return False
    else:
        return False

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
        'filter_record': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': filter_record_error
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
        'file_error': {
            'level': settings.LEVEL_LOG,
            'filters': ['filter_record'],
            'class': 'logging.FileHandler',
            'filename': settings.PATH_LOGS+'/webtooth-error.log',
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
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'django.request': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apppatients.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appfiles.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appnavigations.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appimports.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apptasks.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apprecipes.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appproperties.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appadmin.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apphistory.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appinventories.views': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.config': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apppatients.config': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appfiles.config': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appimports.config': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apptasks.config': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apprecipes.config': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'appadmin.config': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apptasks.tasks': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apppatients.query': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apptasks.query': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'apphistory.query': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.signals': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'webtooth.decorators': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'django.db.backends': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
         'django.template': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
        'django.server': {
            'handlers': ['file', 'console','file_error'],
            'level': settings.LEVEL_LOG,
            'propagate': settings.PROPAGATE_LOG,
            'formatter': 'backend',
        },
    },
}
