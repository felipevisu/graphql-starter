import ast
import os
from datetime import timedelta
from pathlib import Path
from typing import List

import dj_database_url
from dotenv import load_dotenv

load_dotenv()


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = get_bool_from_env("DEBUG", True)

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps
    "graphqlstarter.blog",
    # libs
    "django_filters",
    "graphene_django",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "graphqlstarter.urls"

TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "graphqlstarter.wsgi.application"


DATABASE_CONNECTION_DEFAULT_NAME = "default"

DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "")
DB_HOST = os.environ.get("DB_HOST", "")

DATABASES = {
    DATABASE_CONNECTION_DEFAULT_NAME: dj_database_url.config(
        default=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}",
        conn_max_age=600,
    ),
}

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

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

FTP_USER = os.environ.get("FTP_USER")
FTP_PASSWORD = os.environ.get("FTP_PASSWORD")
FTP_HOST = os.environ.get("FTP_HOST")
FTP_PORT = os.environ.get("FTP_PORT")
FTP_PATH = os.environ.get("FTP_PATH")
FTP_STORAGE_LOCATION = (
    f"ftp://{FTP_USER}:{FTP_PASSWORD}@{FTP_HOST}:{FTP_PORT}{FTP_PATH}"
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

DEFAULT_FILE_STORAGE = "storages.backends.ftp.FTPStorage"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATICFILES_DIRS = [
    ("images", os.path.join(PROJECT_ROOT, "graphqlstarter", "static", "images"))
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

GRAPHENE = {
    "SCHEMA": "graphqlstarter.graphql.schema.schema",
    "SCHEMA_OUTPUT": "schema.graphql",
    "SCHEMA_INDENT": 2,
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}
GRAPHQL_MIDDLEWARE: List[str] = []
PLAYGROUND_ENABLED = DEBUG

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]


JWT_EXPIRE = False
JWT_TTL_ACCESS = timedelta(seconds=10)
JWT_TTL_APP_ACCESS = timedelta(seconds=10)
JWT_TTL_REFRESH = timedelta(days=30)
JWT_TTL_REQUEST_EMAIL_CHANGE = timedelta(seconds=3600)
