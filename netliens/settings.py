"""
Django settings for netliens project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webbook'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'netliens.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'netliens.wsgi.application'

# Required to use AbstractUser Object
# https://docs.djangoproject.com/fr/3.1/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'webbook.User'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': "netliens",
        'HOST': "mongodb"
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# LOGGER
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {message}',
            'style': '{'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{'
        },
    },
    'handlers': {
        'file_logging': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 5,
            'maxBytes': 5000000,
            'filename': 'django-db.log'
        },
        'views_logging': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 5,
            'maxBytes': 5000000,
            'filename': 'django-views.log'
        },
        # This one is only to avoid QuerySet logs
        'db_logging': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 5,
            'maxBytes': 5000000,
            'filename': 'django.log'
        }
    },
    'loggers': {
        'models': {
            'handlers': ['file_logging'],
            'level': 'DEBUG',
            'propagate': True
        },
        'views': {
            'handlers': ['views_logging'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.db': {
            'handlers': ['db_logging'],
            'level': 'INFO',
            'propagate': False
        }
    }
}


# Internationalization
"""
https://docs.djangoproject.com/en/3.0/topics/i18n/
https://docs.djangoproject.com/fr/3.0/topics/i18n/translation/
https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django/1874201-linternationalisation
python3 manage.py makemessages -all : Update element in code
python3 manage.py makemessages -l fr : Create folder for a new traduction in select language
"""
LANGUAGE_CODE = 'en'
#TODO: Check how to show date time function of location in app automatically
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
gettext = lambda x: x
LANGUAGES = (
    ('en', gettext('English')),
    ('fr', gettext('French')),
)
MIDDLEWARE_CLASSES = (
   'django.middleware.locale.LocaleMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
   "django.template.context_processors.i18n",
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = "/django_app/static"

# Media files (Images)
MEDIA_URL = 'media/'
MEDIA_ROOT = "/django_app/media"


# URLS
# - Login
LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = "/account/logout"
LOGOUT_REDIRECT_URL = '/'
# - Errors
# https://docs.djangoproject.com/fr/2.2/topics/http/views/
handler404 = 'annuaire.views.errors.error404'
handler500 = 'annuaire.views.errors.error500'
handler403 = 'annuaire.views.errors.error403'
handler400 = 'annuaire.views.errors.error400'