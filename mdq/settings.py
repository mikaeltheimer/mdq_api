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
TEMPLATE_DIRS = (
    BASE_DIR + '/templates/'
)

ALLOWED_HOSTS = []

APPEND_SLASH = True


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
    'haystack',

    # Admin plugins
    #'suit',
    'django_extensions',
    'south',

    # MDQ Apps
    'accounts',
    'motsdits',
    'api',

    'corsheaders',

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
    'corsheaders.middleware.CorsMiddleware',
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

# Search settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://es.motsditsquebec.com:9200/',    # es.motsditsquebec.com
        'INDEX_NAME': 'haystack',
    },
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

AUTH_USER_MODEL = 'accounts.MDQUser'

# Set some vars to represent the two types of items
WHAT, WHERE = 'what', 'where'

# Default distance we search at
DEFAULT_SEARCH_RADIUS = 100

# Configure CORS
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'X-CSRFToken'
)

CORS_ORIGIN_ALLOW_ALL = True


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.DefaultPermissions',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'per_page',  # Allow client to override, using `?per_page=xxx`.
    'MAX_PAGINATE_BY': 100,            # Maximum limit allowed when using `?per_page=xxx`.

    # Configure user throttling
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.UserRateThrottle',
    ),

    # Set throttle rate to fairly high
    'DEFAULT_THROTTLE_RATES': {
        'user': '25/second'
    }

}

# Mots-dits news
NEWS_CREATED_MOTDIT = 'motdit-created'
NEWS_UPDATED_MOTDIT = 'motdit-updated'
NEWS_LIKED_MOTDIT = 'motdit-liked'
NEWS_FAVOURITED_MOTDIT = 'motdit-favourited'

# Photo news
NEWS_LIKED_PHOTO = 'photo-liked'

# Story news
NEWS_LIKED_STORY = 'story-liked'

NEWS_ASKED_QUESTION = 'question-asked'
NEWS_ANSWERED_QUESTION = 'question-answered'

NEWS_TYPE_CHOICES = (

    # Mots-dits news
    (NEWS_CREATED_MOTDIT, 'Created Mot-Dit'),
    (NEWS_UPDATED_MOTDIT, 'Updated Mot-Dit'),
    (NEWS_LIKED_MOTDIT, 'Liked Mot-Dit'),
    (NEWS_FAVOURITED_MOTDIT, 'Favourited Mot-Dit'),

    # Photo news
    (NEWS_LIKED_PHOTO, 'Liked Photo'),

    # Story news
    (NEWS_LIKED_STORY, 'Liked Story'),

    (NEWS_ASKED_QUESTION, 'Asked a Question'),
    (NEWS_ANSWERED_QUESTION, 'Answered a Question'),

)


# Allow for local configuration
try:
    from local_settings import *
except ImportError:
    pass


if not DEBUG:
    # When in production, default to storing everyhing in Amazon S3
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = "AKIAIMQSPV3SJ4Y7GI3Q"
    AWS_SECRET_ACCESS_KEY = "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"
    AWS_STORAGE_BUCKET_NAME = "motsditsv2"
    AWS_QUERYSTRING_AUTH = False
else:
    pass
