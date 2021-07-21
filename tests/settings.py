"""
Django settings for test_app
"""

import os

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()

ADMIN_URL = "admin/"

SECRET_KEY = "F5#Dw936jRy%uy76f$Sqk$**dXS#8zPwrpBP84k$8NgBpnv4*g"

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "django_extensions",
    "replicat_documents",
    "test_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tests.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

POSTGRES_USER = env("POSTGRES_USER")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD")
POSTGRES_HOST = env("POSTGRES_HOST")
POSTGRES_PORT = env("POSTGRES_PORT")
POSTGRES_DB = env("POSTGRES_DB")
DATABASES = {"default": f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# MEDIA AND STATIC
# https://docs.djangoproject.com/en/3.2/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, "test_core/mediaroot")

# URL that handles the media served from MEDIA_ROOT. Use a trailing slash.
# https://docs.djangoproject.com/en/3.2/ref/settings/#media-url
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# https://docs.djangoproject.com/en/3.2/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, "test_core/staticroot")

# URL prefix for static files
# https://docs.djangoproject.com/en/3.2/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/3.2/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
