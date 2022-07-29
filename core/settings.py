import json
import os
from pathlib import Path

# Get Wahlrechner theme
THEME = os.getenv("WAHLRECHNER_THEME", "theme_default")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DJANGO_DEBUG", 0)))

ALLOWED_HOSTS = json.loads(os.getenv("DJANGO_ALLOWED_HOSTS"))
CSRF_TRUSTED_ORIGINS = json.loads(os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS"))

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wahlrechner",
    "import_export",
    "colorfield",
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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / f"themes/{THEME}/templates",
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": "db",
        "PORT": os.getenv("MYSQL_PORT"),
    }
}

# Password validation

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

LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "de")

TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "Europe/Berlin")

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static and media files (CSS, JavaScript, Images)

MEDIA_URL = "/media/"
MEDIA_ROOT = "/code/media/"

STATIC_URL = "/static/"
STATIC_ROOT = "/code/assets/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / f"themes/{THEME}/static",
]

# SSL-Encryption

SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", 0))
SESSION_COOKIE_SECURE = bool(int(os.getenv("DJANGO_SESSION_COOKIE_SECURE", 1)))
