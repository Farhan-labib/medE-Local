"""
Django settings for medE project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!p!jwnxnk_nf)5psc4-bu2n(^so-zk0#-c_t=gl97a-*4(rs0@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "192.168.0.106", "mede-dxyxn.ondigitalocean.app", "192.168.0.104", "192.168.0.110", "192.168.0.112", "192.168.0.101", "localhost", "178.128.83.106"]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1870050

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'Home',
    'products',
    'authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'medE.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'defaultdb',
        'USER': 'doadmin',
        'PASSWORD': 'AVNS_L16sgy-KIK4T-8-Yc--',  # your database password
        'HOST': 'db-mysql-nyc3-19803-do-user-15848017-0.c.db.ondigitalocean.com',
        'PORT': '25060',
        'OPTIONS': {
            'ssl': {
                'ca': '/medE/ca-certificate.crt'  # replace with path to your CA certificate file
            }
        }
    }
}


LOGOUT_REDIRECT_URL = 'home'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

#For Users
AUTH_USER_MODEL = 'authentication.UserProfile'
#For Admins
# AUTH_USER_MODEL = 'auth.user'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # ... other authentication backends if any ...
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR,]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Changed to a different directory name

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TWILIO_ACCOUNT_SID = 'AC9208a41b026e1730f6190c699c29a6cd'
TWILIO_AUTH_TOKEN = '4bc4931a223f7048f8c0567e1b66a69c'
TWILIO_PHONE_NUMBER = '+17409211140'

if DEBUG:
    MIDDLEWARE.append('livereload.middleware.LiveReloadScript')
ROOT_URLCONF = 'medE.urls'
