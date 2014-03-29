"""
Django settings for MDQ project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '362-qtrxq#-o)i^tt(fc_$#^%4)wzxy)tvfxn!ynp*^n_3k%l+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (

    # Application plugins
    'storages',
    'geoposition',

    # API plugins
    'rest_framework',
    'provider',
    'provider.oauth2',
    'django_filters',
    #'rest_framework.authtoken', # enable when setting up token-based authentication

    # Admin plugins
    #'suit',
    'django_extensions',
    'south',

    # MDQ Apps
    'accounts',
    'motsdits',
    'api',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mdq.urls'

WSGI_APPLICATION = 'mdq.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'motsdits2',
        'USER': 'stephen',
        'PASSWORD': 'goose',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},  # Improve performance once DB is settled by removing this
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/home/motsdits/api/static/'

STATIC_URL = '/static/'

# Default to storing everyhing in Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = "AKIAIMQSPV3SJ4Y7GI3Q"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "motsditsv2"
AWS_QUERYSTRING_AUTH = False

AUTH_USER_MODEL = 'accounts.MDQUser'

# Set some vars to represent the two types of items
WHAT, WHERE = 'what', 'where'

# Configure CORS
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'X-CSRFToken'
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'count',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.
}


# Allow for local configuration
try:
    from local_settings import *
except ImportError:
    pass
