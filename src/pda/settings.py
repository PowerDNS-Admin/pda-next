"""
Django settings for PDA project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import environ
import os
from django.utils.translation import gettext_lazy
from pathlib import Path
from config import AppSettings, load_settings

# Define the default root path of the project based on the location of this file
ROOT_PATH: Path = Path(__file__).parent.parent.parent

# Define the default environment file path to load settings from
ENV_FILE_PATH: str = os.getenv('PDA_ENV_FILE', str(ROOT_PATH / '.env'))

# Load various Django settings from an environment file and the local environment
SETTINGS: AppSettings = load_settings(ENV_FILE_PATH)

env = environ.Env()
env.read_env(os.path.join(ROOT_PATH, ".env"))

SECRET_KEY = SETTINGS.secret_key
DEBUG = SETTINGS.debug
ALLOWED_HOSTS = SETTINGS.allowed_hosts

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
]

# Put your third-party apps here
THIRD_PARTY_APPS = [
    "allauth",  # allauth account/registration management
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "allauth_2fa",
    "rest_framework",
    "drf_spectacular",
    "rest_framework_api_key",
    "celery_progress",
    "waffle",
]

# Put your project-specific apps here
PROJECT_APPS = [
    "apps.users.apps.UserConfig",
    "apps.api.apps.APIConfig",
    "apps.web",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "apps.web.locale_middleware.UserLocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "waffle.middleware.WaffleMiddleware",
]

ROOT_URLCONF = "pda.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [SETTINGS.template_path, ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.web.context_processors.project_meta",
                # this line can be removed if not using Google Analytics
                "apps.web.context_processors.google_analytics_id",
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [SETTINGS.template_path, ],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'pda.jinja2.JinjaEnvironment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "apps.web.context_processors.project_meta",
                # this line can be removed if not using Google Analytics
                "apps.web.context_processors.google_analytics_id",
            ],
        },
    },
]

WSGI_APPLICATION = "pda.wsgi.application"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {}

if isinstance(SETTINGS.db_url, str) and len(SETTINGS.db_url.strip()):
    DATABASES['default'] = env.db_url_config(url=SETTINGS.db_url)

    if 'NAME' in DATABASES['default'] and isinstance(DATABASES['default']['NAME'], str) and len(
            DATABASES['default']['NAME'].strip()):
        DATABASES['default']['NAME'] = os.path.join(SETTINGS.root_path, DATABASES['default']['NAME'])
else:
    db: dict = {}
    db_engine: str = SETTINGS.db_engine.lower()

    if db_engine == 'sqlite':
        db = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': SETTINGS.db_path,
        }

    elif db_engine in ['mysql', 'postgresql']:
        db = {
            'HOST': SETTINGS.db_host,
            'PORT': SETTINGS.db_port,
            'USER': SETTINGS.db_user,
            'PASSWORD': SETTINGS.db_password,
            'NAME': SETTINGS.db_name,
        }

        if db_engine == 'mysql':
            db['ENGINE'] = 'django.db.backends.mysql'
            db['OPTIONS'] = {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }

        elif db_engine == 'postgresql':
            db['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

    else:
        raise ValueError(f'Invalid database engine specified: {db_engine}')

    if bool(db):
        DATABASES['default'] = db
    else:
        raise ValueError('Invalid database configuration detected')

# Auth / login stuff

# Django recommends overriding the user model even if you don't think you need to because it makes
# future changes much easier.
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Allauth setup

ACCOUNT_ADAPTER = 'apps.users.adapter.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# User signup configuration: change to "mandatory" to require users to confirm email before signing in.
# or "optional" to send confirmation emails but not require them
ACCOUNT_EMAIL_VERIFICATION = SETTINGS.account_email_verification

ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS = False

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# enable social login
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGE_COOKIE_NAME = 'pdns_admin_language'
LANGUAGES = [
    ('en', gettext_lazy('English')),
    ('fr', gettext_lazy('French')),
]
LOCALE_PATHS = (os.path.join(SETTINGS.src_path, 'locale'),)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(SETTINGS.src_path, 'static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(SETTINGS.src_path, 'static')]

# uncomment to use manifest storage to bust cache when file change
# note: this may break some image references in sass files which is why it is not enabled by default
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(SETTINGS.root_path, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# future versions of Django will use BigAutoField as the default, but it can result in unwanted library
# migration files being generated, so we stick with AutoField for now.
# change this to BigAutoField if you're sure you want to use it and aren't worried about migrations.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Email setup

# use in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# use in production
# see https://github.com/anymail/django-anymail for more details/examples
# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# Django sites

SITE_ID = 1

# DRF config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('apps.api.permissions.IsAuthenticatedOrHasUserAPIKey',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'PowerDNS Admin',
    'DESCRIPTION': 'PowerDNS Admin',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'displayOperationId': True,
    },
    'PREPROCESSING_HOOKS': [
        'apps.api.schema.filter_schema_apis',
    ],
    'APPEND_COMPONENTS': {
        'securitySchemes': {'ApiKeyAuth': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    },
    'SECURITY': [
        {
            'ApiKeyAuth': [],
        }
    ],
}

# Celery setup (using redis)
if 'REDIS_URL' in env:
    REDIS_URL = env('REDIS_URL')
elif 'REDIS_TLS_URL' in env:
    REDIS_URL = env('REDIS_TLS_URL')
else:
    REDIS_HOST = env('REDIS_HOST', default='localhost')
    REDIS_PORT = env('REDIS_PORT', default='6379')
    REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

if REDIS_URL.startswith('rediss'):
    REDIS_URL = f'{REDIS_URL}?ssl_cert_reqs=none'

CELERY_BROKER_URL = CELERY_RESULT_BACKEND = REDIS_URL

PROJECT_METADATA = {
    'NAME': gettext_lazy('PowerDNS Admin'),
    'URL': 'http://demo.powerdnsadmin.org',
    'DESCRIPTION': gettext_lazy('PowerDNS Admin'),
    'IMAGE': 'https://',
    'KEYWORDS': 'pdns, powerdns, pda, admin, manage, console, dns, domain, nameserver, recursor, cache, authoritative, '
                + 'dnssec, app, ui',
    'CONTACT_EMAIL': 'admin@powerdnsadmin.org',
}

USE_HTTPS_IN_ABSOLUTE_URLS = False  # set this to True in production to have URLs generated with https instead of http

ADMINS = [('Matt Scott', 'admin@powerdnsadmin.org')]

# Add your Google Analytics ID to the environment to connect to Google Analytics
GOOGLE_ANALYTICS_ID = env('PDA_GOOGLE_ANALYTICS_ID', default='')

# Sentry setup

# populate this to configure sentry. should take the form: 'https://****@sentry.io/12345'
SENTRY_DSN = env('PDA_SENTRY_DSN', default='')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} "{name}" {message}',
            'style': '{',
            'datefmt': '%d/%b/%Y %H:%M:%S',  # match Django server time format
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
        'pda': {
            'handlers': ['console'],
            'level': env('PDNS_ADMIN_LOG_LEVEL', default='INFO'),
        },
    },
}
