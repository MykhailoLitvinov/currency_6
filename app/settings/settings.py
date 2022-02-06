"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import environ
from datetime import timedelta

from celery.schedules import crontab
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse, reverse_lazy

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    RABBITMQ_DEFAULT_USER=(str, 'guest'),
    RABBITMQ_DEFAULT_PASS=(str, 'guest'),
    RABBITMQ_DEFAULT_PORT=(str, '5672'),
    RABBITMQ_DEFAULT_HOST=(str, 'localhost'),

    POSTGRES_HOST=(str, 'localhost'),
    POSTGRES_PORT=(str, '5432'),

    MEMCACHED_HOST=(str, 'localhost'),
    MEMCACHED_PORT=(str, '11211'),
)

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'debug_toolbar',
    'rangefilter',
    'import_export',
    'storages',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',

    'currency',
    'account',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'currency.middlewares.RequestResponseTimeMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'settings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# STATIC_ROOT = BASE_DIR.parent / 'static_content' / 'static'
STATIC_ROOT = '/tmp/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'static_content' / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587  # smtp, http: 80, https: 443
# EMAIL_HOST_USER = 'testtestapp454545@gmail.com'
# EMAIL_HOST_PASSWORD = 'qwerty123456qwerty'
DEFAULT_FROM_EMAIL = 'testtestapp454545@gmail.com'

LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('login')

AUTH_USER_MODEL = 'account.User'

# docker
if DEBUG:
    import os  # only if you haven't already imported this
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

# custom settings
DOMAIN = 'localhost:8000'  # TODO
HTTP_SCHEMA = 'http'  # TODO

# CELERY_BROKER_URL = 'amqp://localhost'
# CELERY_BROKER_URL = 'memory://localhost/'
CELERY_BROKER_URL = f'amqp://{env("RABBITMQ_DEFAULT_USER")}:' \
                    f'{env("RABBITMQ_DEFAULT_PASS")}@' \
                    f'{env("RABBITMQ_DEFAULT_HOST")}:{env("RABBITMQ_DEFAULT_PORT")}//'
# amqp, localhost, port=5672, user=guest, password=guest
CELERY_BEAT_SCHEDULE = {
    'parse_privatbank': {
        'task': 'currency.tasks.parse_privatbank',
        'schedule': crontab(minute='*/1'),
        # 'schedule': crontab(minute='*/15'),
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (  # 403
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    # 'DEFAULT_PAGINATION_CLASS': '',
    'DEFAULT_THROTTLE_RATES': {
        'currency': '60/min',
        # 'user': '1000/day',
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': f'{env("MEMCACHED_HOST")}:{env("MEMCACHED_PORT")}',
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:63342/",
]

# AWS_S3_REGION_NAME = 'fra1'
# AWS_S3_ENDPOINT_URL = 'https://hhhhjhj.fra1.digitaloceanspaces.com/'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = 'DHLQ4ECCUK543W6PRD6B'
# AWS_SECRET_ACCESS_KEY = 'EGVSCbm0bJevs8isPRkmOatLL+YtlivEqjLfHd4W8pw'
# AWS_STORAGE_BUCKET_NAME = 'media'
# MEDIA_URL = 'https://hillel-test.fra1.digitaloceanspaces.com/media/'
# AWS_DEFAULT_ACL = 'public-read'

'''
1. email + password + confirm password (get email)
2. email (get email) + password + confirm password
3. email (get email) 7 days
4. phone, passport, code (confirm) + login

1. form (email, password, confirm password)
2. send email with confirmation link
3. Activation endpoint
'''
