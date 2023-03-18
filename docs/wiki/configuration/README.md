# PDA Next

## Configuration Guide

### Startup Configuration

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

#### Application Startup Settings

> PDA_ACCOUNT_EMAIL_REQUIRED | type = bool
 
Default: False

Determine whether the user is required to provide an email address during registration.

This setting must be set to True if `PDA_ACCOUNT_EMAIL_VERIFICATION` is set to "mandatory".

See https://django-allauth.readthedocs.io/en/latest/configuration.html for more information.

> PDA_ACCOUNT_EMAIL_VERIFICATION | type = string

Options: mandatory, optional, none \
Default: 'none'

Determines the e-mail verification method during signup – choose one of "mandatory", "optional", or "none".

Setting this to “mandatory” requires PDA_ACCOUNT_EMAIL_REQUIRED to be True

When set to “mandatory” the user is blocked from logging in until the email address is verified. Choose “optional”
or “none” to allow logins with an unverified e-mail address. In case of “optional”, the e-mail verification mail
is still sent, whereas in case of “none” no e-mail verification mails are sent.

See https://django-allauth.readthedocs.io/en/latest/configuration.html for more information.

> PDA_ACCOUNT_AUTHENTICATION_METHOD | type = string

Options: username_email, email, username \
Default: 'username_email'

Specifies the login method to use – whether the user logs in by entering their username,
e-mail address, or either one of both.

Setting this to “email” requires `PDA_ACCOUNT_EMAIL_REQUIRED` to be True

See https://django-allauth.readthedocs.io/en/latest/configuration.html for more information.

> PDA_ADMIN_EMAIL | type = string

Default: 'admin@yourdomain.com'

Should be set to the e-mail address of the site administrator.

See https://docs.djangoproject.com/en/4.1/ref/settings/#admins for more information.

> PDA_ADMIN_FROM_EMAIL | type = string

Default: 'noreply@yourdomain.com'

Should be set to the e-mail address that should be used as the sender of error e-mails sent by the application
to administrators.

> PDA_ADMIN_NAME | type = string

Default: 'Admin'

Should be set to the name of the site administrator.

See https://docs.djangoproject.com/en/4.1/ref/settings/#admins for more information.

> PDA_ALLOWED_HOSTS | type = string

Default: '*'

A list of strings separated by commas that represent the host/domain names that this Django site can serve.
This is a security measure to prevent an attacker from poisoning caches and password reset emails with links to
malicious hosts by submitting requests with a fake HTTP Host header, which is possible even under many
seemingly-safe web server configurations.

See https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts for more information.

> PDA_CONFIG_PATH | type = string

Default: '/etc/pda/config.yml'

The path to the YAML configuration file that should be used to provide additional non-environment defined
configuration settings for the application.

A template for this file can be found at `config/config.tpl.yml`.

> PDA_CSRF_COOKIE_SECURE | type = bool

Default: True

Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be marked as “secure”,
which means browsers may ensure that the cookie is only sent with an HTTPS connection.

> PDA_DB_ENGINE | type = string

Options: mysql, postgres, sqlite \
Default: 'sqlite'

The database engine to use for the application. Currently, there are three supported database engines: MySQL,
PostgreSQL, and SQLite. This setting is only used if `PDA_DB_URL` is not set.

> PDA_DB_HOST | type = string

Default: ''

The host to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

> PDA_DB_NAME | type = string

Default: ''

The name of the database to use for the application. This setting is only used if `PDA_DB_URL` is not set.

> PDA_DB_PASSWORD | type = string

Default: ''

The password to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

> PDA_DB_PATH | type = string

Default: '/var/lib/pda/pda.db'

The path to the SQLite database file to use for the application. This setting is only used if `PDA_DB_URL`
is not set.

> PDA_DB_PORT | type = int | None

Default: None

The port to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

> PDA_DB_URL | type = string

Default: 'sqlite:///pda.db'

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

> PDA_DB_USER | type = string

Default: ''

The username to use for the database connection. This setting is only used if `PDA_DB_URL` is not set.

### Runtime Configuration

The configuration settings listed in this section are used during runtime by various application features. Configuration
settings are only placed here if the setting isn't required to bootstrap the application during initialization.

**More coming soon!**