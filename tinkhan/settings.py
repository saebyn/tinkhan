# Django settings for tinkhan project.
import os
import urlparse
from datetime import timedelta
import os.path
PROJECT_BASE = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('John Weaver', 'john@saebyn.info',),
)

MANAGERS = ADMINS

DATABASES = {}

# Heroku database settings
import dj_database_url
DATABASES['default'] = dj_database_url.config(default='postgres://postgres@localhost:5432/tinkhan')


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# Not used.
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://tinkhan-static2.s3-website-us-east-1.amazonaws.com/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_rs0rcf01%x0j@lygn@2gunz%=f=a5a131pzqh1m%^q=xo-)m3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tinkhan.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tinkhan.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_BASE, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    'gunicorn',
    'kombu.transport.django',
    'djcelery',
    'storages',
    'south',
    'seacucumber',

    'errortemplates',
    'tos',
    'registration',
    'profiles',
    'bootstrapform',
    'html5forms',

    # our apps
    'khan',
    'tincan_exporter',
    'tinkhan_app',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'tinkhan_app.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 3

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379/1')
REDIS_CONFIG = urlparse.urlparse(REDIS_URL)
try:
    REDIS_DB = int(REDIS_CONFIG.path[1:])
except ValueError:
    REDIS_DB = 0

# celery settings
BROKER_URL = REDIS_URL
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_RESULT_BACKEND = REDIS_URL


CELERYBEAT_SCHEDULE = {
    'update-badge-categories': {
        'task': 'khan.tasks.update_badge_categories',
        'schedule': timedelta(hours=2),
        'args': (),
    },
    'update-topic-tree': {
        'task': 'khan.tasks.update_topic_tree',
        'schedule': timedelta(hours=2),
        'args': (),
    },
}

CELERY_TIMEZONE = 'UTC'

import djcelery
djcelery.setup_loader()

# cache configuration

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (REDIS_CONFIG.hostname, REDIS_CONFIG.port),
        'OPTIONS': {
            'DB': REDIS_DB,
            'PASSWORD': REDIS_CONFIG.password,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        }
    }
}

# static storage config
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
# see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Expires': 'Fri, 1 Apr 2022 12:00:00 GMT',
    'Cache-Control': 'max-age=86400',
}

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

EMAIL_BACKEND = 'seacucumber.backend.SESBackend'

TINKHAN_OAUTH_CONSUMER_KEY = ''
TINKHAN_OAUTH_CONSUMER_SECRET = ''

FROM_EMAIL = 'Tin Khan Robot <tinkhan@saebyn.info>'
DEFAULT_FROM_EMAIL = FROM_EMAIL
SERVER_EMAIL = FROM_EMAIL

try:
    from settings_local import *
except ImportError:
    pass
