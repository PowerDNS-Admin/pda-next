"""
Django settings for PDA project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from django.utils.translation import gettext_lazy
from config import settings

SECRET_KEY = settings.secret_key
DEBUG = settings.debug
ALLOWED_HOSTS = settings.allowed_hosts

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
        "DIRS": [settings.template_path, ],
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
        'DIRS': [settings.template_path, ],
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

if isinstance(settings.db_url, str) and len(settings.db_url.strip()):
    import environ
    env = environ.Env()
    DATABASES['default'] = env.db_url_config(url=settings.db_url)

    if 'NAME' in DATABASES['default'] and isinstance(DATABASES['default']['NAME'], str) and len(
            DATABASES['default']['NAME'].strip()):
        DATABASES['default']['NAME'] = os.path.join(settings.root_path, DATABASES['default']['NAME'])
else:
    db: dict = {}
    db_engine: str = settings.db_engine.lower()

    if db_engine == 'sqlite':
        db = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': settings.db_path,
        }

    elif db_engine in ['mysql', 'postgresql']:
        db = {
            'HOST': settings.db_host,
            'PORT': settings.db_port,
            'USER': settings.db_user,
            'PASSWORD': settings.db_password,
            'NAME': settings.db_name,
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
ACCOUNT_AUTHENTICATION_METHOD = settings.account_authentication_method
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False

# User signup configuration: change to "mandatory" to require users to confirm email before signing in.
# or "optional" to send confirmation emails but not require them
ACCOUNT_EMAIL_VERIFICATION = settings.account_email_verification

ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS = False

AUTHENTICATION_BACKENDS = (
    # Needed to log in by username in Django admin, regardless of `allauth`
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

LANGUAGE_CODE = settings.language_code
LANGUAGE_COOKIE_NAME = settings.language_cookie_name
LANGUAGES = [
    ('en', gettext_lazy('English')),
    ('fr', gettext_lazy('French')),
]
LOCALE_PATHS = (os.path.join(settings.src_path, 'locale'),)

TIME_ZONE = settings.time_zone

USE_I18N = settings.use_i18n

USE_L10N = settings.use_l10n

USE_TZ = settings.use_tz

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(settings.src_path, 'static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(settings.src_path, 'static')]

# uncomment to use manifest storage to bust cache when file change
# note: this may break some image references in sass files which is why it is not enabled by default
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(settings.root_path, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# future versions of Django will use BigAutoField as the default, but it can result in unwanted library
# migration files being generated, so we stick with AutoField for now.
# change this to BigAutoField if you're sure you want to use it and aren't worried about migrations.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Email setup

EMAIL_BACKEND = None
if isinstance(settings.email_backend, str) and len(settings.email_backend.strip()):
    EMAIL_BACKEND = settings.email_backend

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
    'TITLE': settings.site_title,
    'DESCRIPTION': settings.site_description,
    'VERSION': settings.version,
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

REDIS_URL: str | None = None
if isinstance(settings.redis_url, str) and len(settings.redis_url.strip()):
    REDIS_URL = settings.redis_url
elif isinstance(settings.redis_host, str) and len(settings.redis_host.strip()):
    REDIS_HOST = settings.redis_host
    REDIS_PORT = settings.redis_port
    REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

if isinstance(REDIS_URL, str):
    # Disable REDIS SSL cert verification if using rediss:// protocol
    if REDIS_URL.startswith('rediss'):
        REDIS_URL += '?ssl_cert_reqs=none'

    # Celery setup (using redis)
    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = REDIS_URL

PROJECT_METADATA = {
    'NAME': gettext_lazy(settings.site_title),
    'URL': settings.site_url,
    'DESCRIPTION': gettext_lazy(settings.site_description),
    'IMAGE': settings.site_logo,
    'KEYWORDS': 'pdns, powerdns, pda, admin, manage, console, dns, domain, nameserver, recursor, cache, authoritative, '
                + 'dnssec, app, ui',
    'CONTACT_EMAIL': settings.site_email,
}

USE_HTTPS_IN_ABSOLUTE_URLS = settings.use_https_in_absolute_urls

# Setup Site Admin Contacts
ADMINS = [(settings.admin_name, settings.admin_email)]

# Setup Google Analytics
GOOGLE_ANALYTICS_ID = settings.google_analytics_id

# Setup Sentry Exception Tracking
if isinstance(settings.sentry_dsn, str) and len(settings.sentry_dsn.strip()):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(dsn=settings.sentry_dsn, integrations=[DjangoIntegration()])

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
            'level': settings.django_log_level,
        },
        'pda': {
            'handlers': ['console'],
            'level': settings.log_level,
        },
    },
}
