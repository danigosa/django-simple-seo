# This is an example test settings file for use with the Django test suite.
#
# The 'sqlite3' backend requires only the ENGINE setting (an in-
# memory database will be used). All other backends will require a
# NAME and potentially authentication information. See the
# following section in the docs for more information:
#
# https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/
#
# The different databases that Django supports behave differently in certain
# situations, so it is recommended to run the test suite against as many
# database backends as possible.  You may want to create a separate settings
# file for each of the backends you test against.
import os

DEBUG = True
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    },
}

SECRET_KEY = '__secret__'
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'simple_seo',
    'testapp'
)

SEO_USE_CACHE = True
SEO_MODEL_REGISTRY = (
    ('testapp.MyMetadata', ('template_test', )),
)

STATIC_URL = '/static/'
STATIC_ROOT = PROJECT_PATH + STATIC_URL
MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_PATH + MEDIA_URL

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

STATICFILES_DIRS = (
    PROJECT_PATH + '/media/',
)

ROOT_URLCONF = 'simple_seo.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# LOGGING CONFIGURATION WITHOUT SENTRY
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] - (%(module)s) - %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
COVERAGE_BADGE_TYPE = 'drone.io'
COVERAGE_CODE_EXCLUDES = [
    'def __unicode__\(self\):',
    'def get_absolute_url\(self\):',
    'from .* import .*', 'import .*',
    'simple_seo.admin',
    'simple_seo.views',
    'simple_seo.models',
    'simple_seo.__pycache__',
    'simple_seo.templatetags.__pycache__'
]
COVERAGE_REPORT_HTML_OUTPUT_DIR = 'tests_html'

try:
    from local_settings import *
except ImportError:
    pass