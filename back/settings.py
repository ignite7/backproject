"""
Django settings for back project.
"""

# Django
from django.contrib.auth.hashers import Argon2PasswordHasher

# Utilities
import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read the .env file
env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = [env('ALLOWED_HOSTS')]
HOST = 'https://{}'.format(env('ALLOWED_HOSTS'))

# Title
TITLE = 'The Back Project | '

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'bootstrap4',
    'crispy_forms',
    'storages',
    'gunicorn'
]

LOCAL_APPS = [
    'models',
    'api.services',
    'api.auths',
    'ui',
    'ui.templatetags'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = env('ROOT_URLCONF')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = env('WSGI_APPLICATION')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'sql_mode': env('DB_MODE')
        },
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# AWS
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
}

# Models
AUTH_USER_MODEL = env('AUTH_USER_MODEL')

# Password validation
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher'
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Argon2 parameters
Argon2PasswordHasher.time_cost = 5
Argon2PasswordHasher.memory_cost = 1024
Argon2PasswordHasher.parallelism = 5

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = 'static'
STATIC_URL = env('STATIC_URL')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Session
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
CSRF_COOKIE_AGE = 3600
CSRF_USE_SESSIONS = True
CSRF_FAILURE_VIEW = 'back.views.handler_csrf_failure'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Configuration email backend
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True

# Django css forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Media settings
MEIA_ROOT = os.path.join(BASE_DIR, env('MEDIA_ROOT'))
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'

# Celery
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_TASK_TIME_LIMIT = 5 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 60

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'models.users.TokensModel',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning'
}
