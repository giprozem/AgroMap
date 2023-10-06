# settings.py - Django Application Configuration

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

from decouple import config

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for the Django application
SECRET_KEY = config('SECRET_KEY').split(',')

# Debug mode (set to True for development, should be False in production)
DEBUG = True

# Allowed hosts for the application
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# Trusted origins for CSRF protection
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS').split(',')

# Installed Django applications
INSTALLED_APPS = [
    'gip',
    'indexes',
    'culture_model',
    'hub',
    'account',
    'ai',
    'auditlog.apps.AuditlogConfig',
]

# Additional installed libraries
INSTALLED_LIB = [
    'jazzmin',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'rest_framework_gis',
    'corsheaders',
    'drf_yasg',
    'leaflet',
    'simple_history',
    'django_extensions',
    'schema_graph',
]

# Merge installed libraries with Django applications
INSTALLED_APPS = INSTALLED_LIB + INSTALLED_APPS

# Middleware settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'account.authentication.AdminLastVisitMiddleware',
    'account.authentication.MyAuditMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'config.urls'

# Template settings
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

# WSGI application entry point
WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', cast=int),
    }
}

# Password validation settings
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

# Language and timezone settings
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Locale paths for translations
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

# Available languages
gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('ru', gettext('Russian')),
    ('ky', gettext('Kyrgyz')),
)

# Default language for model translations
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

# Custom user model
AUTH_USER_MODEL = 'account.MyUser'

# Static and media files settings
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default auto field for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True

# Leaflet map configuration
LEAFLET_CONFIG = {
    "DEFAULT_CENTER": (42.87, 74.59),
    "DEFAULT_ZOOM": 10,
    "MAX_ZOOM": 20,
    "MIN_ZOOM": 3,
    "SCALE": 'both',
    'TILES': [('Google', 'http://{s}.google.com/vt/lyrs=s,m,p&x={x}&y={y}&z={z}',
               {'maxZoom': 20, 'subdomains': ['mt0', 'mt1', 'mt2', 'mt3']}),
              ('OSM', 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}),
              ]
}

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'account.authentication.MyTokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# Jazzmin settings
JAZZMIN_SETTINGS = {
    "site_title": "AgroMap",
    "site_header": "AgroMap",
    "site_brand": "AgroMap",
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "topmenu_links": [
        {"name": _("Giprozem reference database"), "url": "admin:index", "permissions": ["auth.view_user"]},
        {"models": "auth.User"},
    ],
    "language_chooser": True,
    "order_with_respect_to": [
        # Specify the order of your application models here
    ],
}

# Jazzmin UI tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

# Apache Kafka configuration
KAFKA_HOST_PORT = config('KAFKA_HOST_PORT')
