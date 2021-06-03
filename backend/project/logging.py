"""
Logging settings for ambassador project.

Must be at the same directory as the settings.py file.

Documentation
https://docs.djangoproject.com/en/3.2/topics/logging/
"""
import os
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / 'logs'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {process:d} {thread:d} '
                      '{message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },  # formatters
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGS_DIR.joinpath('debug.log'),
            'when': 'midnight',
            'backupCount': 30,
        },
    },  # handlers
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO').upper(),
        },
        # 'app_name': {
        #     'handlers': ['console', 'file'],
        #     'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG').upper(),
        #     'propagate': False,  # required to eliminate duplication on root
        # },
    },  # loggers
}  # logging
