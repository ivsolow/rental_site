"""
Django settings for equipment_rental_site project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.getenv("DEBUG", default=0))

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', '31.129.104.187']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_extensions',
    'drf_spectacular',
    'corsheaders',

    'equipment',
    'cart',
    'feedback',
    'rentals',
    'users',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'equipment_rental_site.urls'

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

WSGI_APPLICATION = 'equipment_rental_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'USER': os.environ.get('POSTGRES_USER'),
    },
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'HOST': 'localhost',
#         'NAME': 'equipment_db',
#         'PASSWORD': 1234,
#         'USER': 'postgres',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501, E701
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa: E501, E701
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa: E501, E701
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa: E501, E701
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

YOOKASSA_ACCOUNT_ID = os.getenv('YOOKASSA_ACCOUNT_ID')
YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'}
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

DJOSER = {
    'DOMAIN': 'frontend.com',
    'SITE_NAME': 'Frontend',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'PASSWORD_VALIDATORS': [],
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserRegistrationSerializer',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-server'
EMAIL_PORT = 1025

AUTH_USER_MODEL = 'users.CustomUser'

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
    }
}


EQUIPMENT_LIST_CACHE_KEY = 'equipment_list'
EQUIPMENT_RETRIEVE_CACHE_KEY = 'equipment_retrieve'
AVAIL_EQUIPMENT_CACHE_KEY = 'available_equipment'
AVAIL_EQUIPMENT_DATES = 'equipment_dates'
CART_LIST_CACHE_KEY = 'cart_list'
RENTALS_CACHE_KEY = 'rentals_list'

# CSRF_TRUSTED_ORIGINS = ['http://0.0.0.0:1337', ]
# REGISTRATION_ENABLED = True
# REGISTRATION_EMAIL_CONFIRM = False
# ACCOUNT_EMAIL_VERIFICATION = 'none'

# CORS_ALLOW_HEADERS = True
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True

# CORS_ORIGIN_WHITELIST = (
#        'localhost:3000',
#         # 'localhost:3000/equipment/3/'
# )


CORS_BACKEND_ADDRESS = os.getenv('CORS_BACKEND_ADDRESS')
CORS_ALLOWED_ORIGINS = [
    CORS_BACKEND_ADDRESS,
]

# CORS_ALLOW_METHODS = [
#     # Добавьте методы, которые разрешены для запросов
#     'DELETE',
#     'GET',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
# ]
