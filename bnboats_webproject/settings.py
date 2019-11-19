"""
Django settings for bnboats_webproject project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config
from dj_database_url import parse as dburl
import re



# re.compile(r'^/robots\.txt$'),

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ADMINS = [('Renan', 'renangasp@gmail.com')]
ADMINS = [('Renan', 'renangaspar@hotmail.com')]
# MANAGERS = [('Renan', 'renangasp@gmail.com')]

# def ignore404errors(record):
#    if record.status_code == 404:
#        return False
#    return True


DEFAULT_LOGGING = {
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '123qwe!@#QWE' #config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #config('DEBUG', default=False, cast=bool)
THUMBNAIL_DEBUG = DEBUG

ALLOWED_HOSTS = ['bnboats.herokuapp.com', '127.0.0.1', 'localhost', 'www.bnboats.com', 'www.bnboats.com.br',
                 'bnboats.com', 'bnboats.com.br', 'qa-bnb.herokuapp.com', 'improve-bnbboats.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Third-Apps
    # 'test_without_migrations',
    'sorl.thumbnail',
    'ckeditor',
    'ckeditor_uploader',

    #Apps
    'bnboats_app',
    'blog',
]

CKEDITOR_UPLOAD_PATH = "uploads/ckeditor/"
CKEDITOR_FILENAME_GENERATOR = 'bnboats_webproject.utils.get_filename'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}

ROOT_URLCONF = 'bnboats_webproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'bnboats_app.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'bnboats_webproject.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

IGNORABLE_404_URLS = [
    re.compile(r'^/robots\.txt$'),
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'./wp-.'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/barcos/.'),
    re.compile(r'.download.'),
    re.compile(r'.operadores.'),
    re.compile(r'./feed/$'),
    re.compile(r'^\.xml$'),
]

MIDDLEWARE = [
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'enforce_host.EnforceHostMiddleware',
]



# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

LOGIN_URL = '/?signin'

default_dburl = 'postgres:///' + os.path.join(BASE_DIR, 'django.db.backends.postgresql_psycopg2')

if config("ENVIRONMENT") == "PROD":
    SECURE_SSL_REDIRECT = True
    ENFORCE_HOST = config('ENFORCE_HOST') #'www.bnboats.com'
    DATABASES = {'default': config('DATABASE_URL', default=default_dburl, cast=dburl), }
else:
    if config("ENVIRONMENT") == "QA":
        SECURE_SSL_REDIRECT = False
        DATABASES = {'default': config('DATABASE_URL_QA', default=default_dburl, cast=dburl), }
    else:
        # SECURE_SSL_REDIRECT = False
        # DATABASES = {
        #     'default': {
        #         'ENGINE': 'django.db.backends.postgresql',
        #         'NAME': 'bnboats',
        #         'USER': 'postgres',
        #         'PASSWORD': 'gaspar1',
        #         'HOST': '127.0.0.1',
        #         'PORT': '5432',
        #     }
        # }

        SECURE_SSL_REDIRECT = False
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'bnboats',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': '127.0.0.1',
                'PORT': '5433',
            }
        }

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# LANGUAGES = [
#     ('en', 'English'),
# ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# STATIC_URL = '/static/'

STATICFILES_DIRS = [
    'static',
]

# MEDIA_URL = '/media/'

# MEDIA_ROOT = 'media'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = "bucket-principal" #"bucket-boats-improve" #config('AWS_S3_BUCKET_NAME') #"bucket-principal"
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None

# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'bnboats_webproject.storage_backends.MediaStorage'
STATIC_URL = '/static/'
MEDIA_URL = 'https://%s/' % (AWS_S3_CUSTOM_DOMAIN)
MEDIA_ROOT = MEDIA_URL
DEFAULT_PAGE = "Home"

STATIC_MEDIA_URL = 'https://%s/static/' % (AWS_S3_CUSTOM_DOMAIN)

BNBOATS_TAX = 1.185 # %
FISHING_STORES_DISCOUNT = 50 # BRL
