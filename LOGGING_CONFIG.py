# Logging Configuration for ISP Billing & ISP System
# Agregar esto al final de settings.py en ambos proyectos

import logging

# Note: Copy this into your settings.py after importing BASE_DIR and DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '[{levelname}] {asctime} {name} '
                '{funcName}:{lineno} - {message}'
            ),
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'INFO',  # Set dynamically in settings.py
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'billing_app': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',  # Set to DEBUG in development
            'propagate': False,
        },
        'isp_app': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',  # Set to DEBUG in development
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file', 'error_file'],
        'level': 'WARNING',  # Set to DEBUG in development
    },
}
