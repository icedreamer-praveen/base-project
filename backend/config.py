import os
from pathlib import Path

import yaml

with open ("config/application-dev.yml", "r") as file:
    config = yaml.safe_load(file)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['django']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['django']['DEBUG']

ALLOWED_HOSTS = ['*']

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': config('DATABASE_ENGINE'),
#         'NAME': config('DATABASE_NAME'),
#         'USER': config('DATABASE_USER'),
#         'PASSWORD': config('DATABASE_PASSWORD'),
#         'PORT': config('DATABASE_PORT'),
#         'HOST': config('DATABASE_HOST'),
#     }
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/staticfiles/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

MEDIA_URL = '/mediafiles/'

STATIC_ROOT  = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

SPECTACULAR_SETTINGS = {
    'TITLE': 'Backend',
    'DESCRIPTION': 'Keep on Backend!',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'CAMELIZE_NAMES': True,
    'SCHEMA_PATH_PREFIX': r'/api/{version}/',
    # 'SCHEMA_PATH_PREFIX_TRIM': True,

    # side car settings
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # OTHER SETTINGS
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },

}

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

if not os.path.exists("./logs"):
    os.mkdir("./logs")

    
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '{asctime} {levelname} [backend, {request_id}] : {name}{message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when' : 'midnight',
            'interval' : 1,
            'filename': f'./logs/backend.log',
            'formatter': 'standard',
            'backupCount' : 30,
            # 'maxBytes' : 100* 1024 * 1024,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
        'propagate': True,
    },
}

JET_DEFAULT_THEME = 'default'
JET_SIDE_MENU_COMPACT = True
JET_THEMES = [
    {
        'theme': 'default',
        'color': '#47bac1',
        'title': 'Default' 
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]