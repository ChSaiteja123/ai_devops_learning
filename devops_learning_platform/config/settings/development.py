"""
Development settings.

These settings are ONLY for local development.
Never use these in production.
"""
from .base import *  # noqa: F401, F403
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

# Debug toolbar — shows SQL queries, request info, cache hits, etc.
# Only activate when the package is actually installed (it's in development.txt,
# not base.txt, so it may be absent in some local setups).
try:
    import debug_toolbar  # noqa: F401
    INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa: F405
except ImportError:
    pass
INTERNAL_IPS = ['127.0.0.1']

# Use SQLite for quick local testing if no DB is set up
# Comment this out to use PostgreSQL locally
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Print emails to the console instead of sending them
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Disable HTTPS requirements
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Show full error tracebacks
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
