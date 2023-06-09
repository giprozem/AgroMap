import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY').split(',')

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = ['https://adminagro.24mycrm.com', 'https://10.118.50.31']

INSTALLED_APPS = [
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
    'gip',
    'indexes',
    'culture_model',
    'hub',
    'account',
    'ai',
]


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
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Русский')),
    ('ky', gettext('Кыргызский')),
    ('en', gettext('Английский')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

AUTH_USER_MODEL = 'account.MyUser'

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

LEAFLET_CONFIG = {
    "DEFAULT_CENTER": (42.87, 74.59),

    "DEFAULT_ZOOM": 10,

    "MAX_ZOOM": 20,

    "MIN_ZOOM": 3,

    "SCALE": 'both',

    'TILES': [('Google', 'http://{s}.google.com/vt/lyrs=s,m,p&x={x}&y={y}&z={z}',
               {'maxZoom': 20,'subdomains':['mt0','mt1','mt2','mt3']}),
              ('OSM', 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}),
              ]

}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}


JAZZMIN_SETTINGS = {
    "site_title": "AgroMap",
    "site_header": "AgroMap",
    "site_brand": "AgroMap",
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "topmenu_links": [
        {"name": _("Эталонная база данных Гипрозем"), "url": "admin:index", "permissions": ["auth.view_user"]},
        {"models": "auth.User"},
    ],
    "language_chooser": True,
    "order_with_respect_to": [
        "account",
        "auth",
        "gip",
        "gip.Contour",
        "gip.LandType",
        "gip.Region",
        "gip.Conton",
        "gip.District",
        "gip.SoilClass",
        "gip.SoilClassMap",
        "gip.SoilProductivity",
        "gip.SoilFertility",
        "indexes",
        "indexes.ActualVegIndex",
        "indexes.IndexCreatingReport",
        "indexes.IndexMeaning",
        "indexes.SciHubImageDate",
        "indexes.SciHubAreaInterest",

        "ai",
        "culture_model",

        "hub"
    ],
}

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
