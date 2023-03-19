# PDA Next

## Configuration Guide

### Environment Configuration

The configuration settings listed in this section are used for initially configuring the application before
initialization. Configuration settings are only placed here if the setting is required to bootstrap the application and
only changes for the deployment environment.

The given setting names are the names of the environment variables that should be set. When these values are
accessed through the `AppSettings` class, they are converted to the appropriate type, converted to all lowercase,
and the prefix `PDA_` is stripped. The default value is the value that will be used if the environment variable
is not set.

The setting name is prefixed with `PDA_` and the environment variable name is converted to all caps.
For example, the setting name `setting_name` would be accessed through the `AppSettings` class
as `AppSettings.setting_name` and the environment variable name would be `PDA_SETTING_NAME`.

#### Application Environment Settings

##### PDA_ACCOUNT_AUTHENTICATION_METHOD | type = string

Options: username_email, email, username \
Default: 'username_email'

Specifies the login method to use – whether the user logs in by entering their username,
e-mail address, or either one of both.

Setting this to “email” requires `PDA_ACCOUNT_EMAIL_REQUIRED` to be True

See https://django-allauth.readthedocs.io/en/latest/configuration.html for more information.

##### PDA_ACCOUNT_EMAIL_REQUIRED | type = bool
 
Default: False

Determine whether the user is required to provide an email address during registration.

This setting must be set to True if `PDA_ACCOUNT_EMAIL_VERIFICATION` is set to "mandatory".

See https://django-allauth.readthedocs.io/en/latest/configuration.html for more information.

##### PDA_ACCOUNT_EMAIL_VERIFICATION | type = string

Options: mandatory, optional, none \
Default: 'none'

Determines the e-mail verification method during signup – choose one of "mandatory", "optional", or "none".

Setting this to “mandatory” requires PDA_ACCOUNT_EMAIL_REQUIRED to be True

When set to “mandatory” the user is blocked from logging in until the email address is verified. Choose “optional”
or “none” to allow logins with an unverified e-mail address. In case of “optional”, the e-mail verification mail
is still sent, whereas in case of “none” no e-mail verification mails are sent.

See https://django-allauth.readthedocs.io/en/latest/configuration.html for more information.

##### PDA_ACCOUNT_USERNAME_REQUIRED | type = bool
 
Default: False

Determine whether the user is required to provide a username during registration.

This setting must be set to True if `PDA_ACCOUNT_AUTHENTICATION_METHOD` is set to "username" or "username_email".

See https://django-allauth.readthedocs.io/en/latest/configuration.html for more information.

##### PDA_ADMIN_EMAIL | type = string

Default: 'admin@yourdomain.com'

Should be set to the e-mail address of the site administrator.

See https://docs.djangoproject.com/en/4.1/ref/settings/#admins for more information.

##### PDA_ADMIN_FROM_EMAIL | type = string

Default: 'noreply@yourdomain.com'

Should be set to the e-mail address that should be used as the sender of error e-mails sent by the application
to administrators.

##### PDA_ADMIN_NAME | type = string

Default: 'Admin'

Should be set to the name of the site administrator.

See https://docs.djangoproject.com/en/4.1/ref/settings/#admins for more information.

##### PDA_ALLOWED_HOSTS | type = string

Default: '*'

A list of strings separated by commas that represent the host/domain names that this Django site can serve.
This is a security measure to prevent an attacker from poisoning caches and password reset emails with links to
malicious hosts by submitting requests with a fake HTTP Host header, which is possible even under many
seemingly-safe web server configurations.

See https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts for more information.

##### PDA_CONFIG_PATH | type = string

Default: '/etc/pda/config.yml'

The path to the YAML configuration file that should be used to provide additional non-environment defined
configuration settings for the application.

A template for this file can be found at `config/config.tpl.yml`.

##### PDA_CSRF_COOKIE_SECURE | type = bool

Default: True

Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be marked as “secure”,
which means browsers may ensure that the cookie is only sent with an HTTPS connection.

##### PDA_DB_ENGINE | type = string

Options: mysql, postgres, sqlite \
Default: 'sqlite'

The database engine to use for the application. Currently, there are three supported database engines: MySQL,
PostgreSQL, and SQLite. This setting is only used if `PDA_DB_URL` is not set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#databases for more information.

##### PDA_DB_HOST | type = string | None

Default: None

The host to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#databases for more information.

##### PDA_DB_NAME | type = string | None

Default: None

The name of the database to use for the application. This setting is only used if `PDA_DB_URL` is not set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#databases for more information.

##### PDA_DB_PASSWORD | type = string | None

Default: None

The password to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#databases for more information.

##### PDA_DB_PATH | type = string

Default: '/var/lib/pda/pda.db'

The path to the SQLite database file to use for the application. This setting is only used if `PDA_DB_URL`
is not set.

##### PDA_DB_PORT | type = int | None

Default: None

The port to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#databases for more information.

##### PDA_DB_URL | type = string

Default: 'sqlite:////var/lib/pda/pda.db'

Defines the database connection string to use for the application. Currently, there are three supported database
engines: MySQL, PostgreSQL, and SQLite.

To set up a MySQL connection using this approach, a connection string like the following can be used:

    mysql://user:password@host:port/database

To set up a PostgreSQL connection using this approach, a connection string like the following can be used:

    postgres://user:password@host:port/database

To set up a SQLite connection using this approach, a connection string like the following can be used:
    
    sqlite:////absolute/path/to/database/file

If you wish to specify a path to the database file that is relative to the project root, you can use the
following connection string:
    
    sqlite:///relative/path/to/database/file

See https://docs.djangoproject.com/en/3.1/ref/settings/#databases for more information.

##### PDA_DB_USER | type = string | None

Default: None

The username to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#databases for more information.

##### PDA_DEBUG | type = bool

Default: False

Determines whether the application should run in debug mode. If this is set to True, the application will
display detailed error pages when an exception occurs.

See https://docs.djangoproject.com/en/3.1/ref/settings/#debug for more information.

##### PDA_DEV_SERVER_ADDRESS | type = string

Default: '0.0.0.0'

The address that the development server should listen on.

##### PDA_DEV_SERVER_PORT | type = int

Default: 8080

The port that the development server should listen on.

##### PDA_EMAIL_BACKEND | type = string | None

Default: None

The e-mail backend to use for sending e-mails. If this is not set, the default e-mail backend will be used.

For simple testing and local development, the `django.core.mail.backends.console.EmailBackend` can be used to send
e-mails to the console.

For production use, the `django.core.mail.backends.smtp.EmailBackend` can be used to send e-mails using an SMTP
server.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-backend for more information.

There are many backend implementations available for Django aside from just those provided directly through Django.
This project uses the `django-anymail` package to provide support for a number of additional e-mail backends. For
more information on the available backends, see the `django-anymail` documentation.

##### PDA_EMAIL_HOST | type = string | None

Default: None

The host to use for the SMTP server that should be used to send e-mails. This setting is only used if
`PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-host for more information.

##### PDA_EMAIL_HOST_PASSWORD | type = string | None

Default: None

The password to use for the SMTP server that should be used to send e-mails. This setting is only used if
`PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-host-password for more information.

##### PDA_EMAIL_HOST_USER | type = string | None

Default: None

The username to use for the SMTP server that should be used to send e-mails. This setting is only used if
`PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-host-user for more information.

##### PDA_EMAIL_PORT | type = int

Default: 587

The port to use for the SMTP server that should be used to send e-mails. This setting is only used if
`PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-port for more information.

##### PDA_EMAIL_SSL_CERTFILE | type = string | None

Default: None

The path to the SSL certificate file to use when connecting to the SMTP server that should be used to send
e-mails. This setting is only used if `PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-ssl-certfile for more information.

##### PDA_EMAIL_SSL_KEYFILE | type = string | None

Default: None

The path to the SSL key file to use when connecting to the SMTP server that should be used to send e-mails.
This setting is only used if `PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-ssl-keyfile for more information.

##### PDA_EMAIL_SUBJECT_PREFIX | type = string | None

Default: '[PDA] '

Subject-line prefix for email messages sent with django.core.mail.mail_admins or django.core.mail.mail_managers.
You’ll probably want to include the trailing space.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-subject-prefix for more information.

##### PDA_EMAIL_TIMEOUT | type = int | None

Default: None

The timeout to use when connecting to the SMTP server that should be used to send e-mails. This setting is
only used if `PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-timeout for more information.

##### PDA_EMAIL_USE_TLS | type = bool

Default: True

Determines whether TLS should be used when connecting to the SMTP server that should be used to send e-mails.
This setting is only used if `PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-use-tls for more information.

##### PDA_EMAIL_USE_SSL | type = bool

Default: False

Determines whether SSL should be used when connecting to the SMTP server that should be used to send e-mails.
This setting is only used if `PDA_EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`.

See https://docs.djangoproject.com/en/3.1/ref/settings/#email-use-ssl for more information.

##### PDA_GOOGLE_ANALYTICS_ID | type = string | None

Default: None

The Google Analytics ID to use for tracking. If this is not set, Google Analytics will not be used.

##### PDA_LOG_LEVEL_APP | type = string

Options: DEBUG, INFO, WARNING, ERROR, CRITICAL \
Default: 'INFO'

The log level that should be used for the application's logging.

See https://docs.djangoproject.com/en/3.1/topics/logging/#configuring-logging for more information.

##### PDA_LOG_LEVEL_DJANGO | type = string

Options: DEBUG, INFO, WARNING, ERROR, CRITICAL \
Default: 'INFO'

The log level that should be used for Django logging.

See https://docs.djangoproject.com/en/3.1/topics/logging/#django-s-logging-configuration for more information.

##### PDA_LOG_PATH | type = string | None

Default: '/var/log/pda/pda.log'

The path to the log file that should be used for the application's logging. If this is not set, the application's
logging will be sent to stdout.

See https://docs.djangoproject.com/en/3.1/topics/logging/#configuring-logging for more information.

##### PDA_LOG_RETENTION | type = int

Default: 30

The number of days that the application's log file should be retained. This setting is only used if `PDA_LOG_PATH`
is set.

##### PDA_LOG_ROTATION | type = string

Options: daily, weekly, monthly \
Default: 'daily'

The rotation that should be used for the application's log file. This setting is only used if `PDA_LOG_PATH` is
set.

##### PDA_LOG_SIZE | type = int

Default: 100000000

The maximum size, in bytes, that the application's log file should be allowed to grow to. This setting is only
used if `PDA_LOG_PATH` is set.

##### PDA_LOG_TO_FILE | type = bool

Default: False

Determines whether the application's logging should be sent to a file. If this is set to `True`, the application's
logging will be sent to the file specified by `PDA_LOG_PATH`.

##### PDA_LOG_TO_SENTRY | type = bool

Default: False

Determines whether the application's logging should be sent to Sentry. If this is set to `True`, the application's
logging will be sent to Sentry.

##### PDA_LOG_TO_STDOUT | type = bool

Default: True

Determines whether the application's logging should be sent to stdout. If this is set to `True`, the application's
logging will be sent to stdout.

##### PDA_LOG_TO_SYSLOG | type = bool

Default: False

Determines whether the application's logging should be sent to syslog. If this is set to `True`, the application's
logging will be sent to syslog.

##### PDA_REDIS_HOST | type = string | None

Default: None

The host that should be used to connect to Redis. This setting is only used if `PDA_REDIS_URL` is not set.

##### PDA_REDIS_PASSWORD | type = string | None

Default: None

The password that should be used to connect to Redis. This setting is only used if `PDA_REDIS_URL` is not set.

##### PDA_REDIS_PORT | type = int

Default: 6379

The port that should be used to connect to Redis. This setting is only used if `PDA_REDIS_URL` is not set.

##### PDA_REDIS_URL | type = string | None

Default: 'redis://127.0.0.1:6379/0'

The URL that should be used to connect to Redis.

##### PDA_ROOT_PATH | type = string

Default: Automatically Detected

The path to the root directory of the application. This setting is automatically detected during initialization
and should not be set manually unless you know what you're doing.

##### PDA_SECRET_KEY | type = string

Default: INSECURE VALUE

The secret key that should be used for the application. This setting is used to provide cryptographic signing,
and should be set to a unique, unpredictable value. To generate a value for this setting, run the following command:

    pda gen_salt

##### PDA_SECURE_HSTS_SECONDS | type = int

Default: 2592000

The number of seconds that the `Strict-Transport-Security` header should be set for. This setting is only used
if the value is set to an integer value greater than 0.

See https://docs.djangoproject.com/en/3.1/ref/middleware/#http-strict-transport-security for more information.

##### PDA_SECURE_HSTS_INCLUDE_SUBDOMAINS | type = bool

Default: True

Determines whether the `Strict-Transport-Security` header should include subdomains. This setting is only used
if `PDA_SECURE_HSTS_SECONDS` is set to an integer value greater than 0.

##### PDA_SECURE_HSTS_PRELOAD | type = bool

Default: True

Determines whether the `Strict-Transport-Security` header should include the `preload` directive. This setting
is only used if `PDA_SECURE_HSTS_SECONDS` is set to an integer value greater than 0.

##### PDA_SECURE_PROXY_SSL_HEADER_NAME | type = string | None

Default: None

The name of the header that should be used to determine whether the request was made over HTTPS. This setting
is only used if `PDA_SECURE_PROXY_SSL_HEADER_VALUE` is set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#secure-proxy-ssl-header for more information.

##### PDA_SECURE_PROXY_SSL_HEADER_VALUE | type = string | None

Default: None

The value of the header that should be used to determine whether the request was made over HTTPS. This setting
is only used if `PDA_SECURE_PROXY_SSL_HEADER_NAME` is set.

See https://docs.djangoproject.com/en/3.1/ref/settings/#secure-proxy-ssl-header for more information.

##### PDA_SECURE_SSL_REDIRECT | type = bool

Default: True

Determines whether the application should redirect all requests to HTTPS.

See https://docs.djangoproject.com/en/3.1/ref/settings/#secure-ssl-redirect for more information.

##### PDA_SENTRY_DSN | type = string | None

Default: None

The DSN that should be used to connect to Sentry. If this is not set, the application's logging will not be
sent to Sentry. This setting is only used if `PDA_LOG_TO_SENTRY` is set to `True`.

##### PDA_SESSION_COOKIE_SECURE | type = bool

Default: True

Whether to use a secure cookie for the session cookie. If this is set to True, the cookie will be marked as
“secure”, which means browsers may ensure that the cookie is only sent under an HTTPS connection.

Leaving this setting off isn’t a good idea because an attacker could capture an unencrypted session cookie
with a packet sniffer and use the cookie to hijack the user’s session.

See https://docs.djangoproject.com/en/3.1/ref/settings/#session-cookie-secure for more information.

##### PDA_SITE_DESCRIPTION | type = string

Default: 'A PowerDNS web interface with advanced features.'

A brief description of the application or it's purpose. This setting is used to provide a description of the
application for use in various places throughout the application.

##### PDA_SITE_EMAIL | type = string

Default: 'pda@yourdomain.com'

The email used for general contact with the organization running the application. This setting is used to
provide a contact email for the application for use in various places throughout the application.

##### PDA_SITE_FROM_EMAIL | type = string

Default: 'pda@yourdomain.com'

The email used for sending emails from the application.

##### PDA_SITE_LOGO | type = string | None

Default: None

The URL of the logo that should be used for the application. This setting is used to provide a logo for the
application for use in various places throughout the application.

##### PDA_SITE_TITLE | type = string

Default: 'PowerDNS Admin'

The title of the application. This setting is used to provide a title for the application for use in various
places throughout the application.

##### PDA_SITE_URL | type = string

Default: 'https://demo.powerdnsadmin.org'

The URL of the application. This setting is used to provide a URL for the application for use in various places
throughout the application.

##### PDA_SRC_PATH | type = string

Default: Automatically set to the `src` directory within the application root path.

The path to the source directory of the application. This setting is automatically populated during initialization
and should not be set manually unless you know what you're doing.

##### PDA_SYSLOG_HOST | type = string | None

Default: None

The host that should be used to connect to syslog. This setting is only used if `PDA_LOG_TO_SYSLOG` is set to
`True`.

##### PDA_SYSLOG_PORT | type = int

Default: 514

The port that should be used to connect to syslog. This setting is only used if `PDA_LOG_TO_SYSLOG` is set to
`True`.

##### PDA_TEMPLATE_PATH | type = string

Default: Automatically set to the `templates` directory within the path `PDA_SRC_PATH`.

The path to the templates directory of the application. This setting is automatically populated during initialization
and should not be set manually unless you know what you're doing.

##### PDA_TIME_ZONE | type = string

Default: 'UTC'

The timezone that should be used for the application. This setting is used to provide a timezone for the
application for use in various places throughout the application. This setting should be set to a valid
timezone name as defined in the `pytz` library.

##### PDA_USE_HTTPS_IN_ABSOLUTE_URLS | type = bool

Default: True

Determines whether absolute URLs should be generated using HTTPS. This setting is used to provide a URL for
the application for use in various places throughout the application.

##### PDA_USE_I18N | type = bool

Default: True

Determines whether the application should use internationalization and localization.

See https://docs.djangoproject.com/en/3.1/topics/i18n/ for more information.

##### PDA_USE_L10N | type = bool

Default: True

Determines whether the application should use localization.

See https://docs.djangoproject.com/en/3.1/topics/i18n/ for more information.

##### PDA_USE_TZ | type = bool

Default: True

Determines whether the application should use timezones.

See https://docs.djangoproject.com/en/3.1/topics/i18n/timezones/ for more information.

### Runtime Configuration

The configuration settings listed in this section are used during runtime by various application features. Configuration
settings are only placed here if the setting isn't required to bootstrap the application during initialization.

**More coming soon!**