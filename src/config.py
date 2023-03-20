import os
import yaml
from pathlib import Path
from pydantic import BaseSettings

ROOT_PATH: Path = Path(__file__).parent.parent
""" The root path of the application which is typically the project repository root path. """

SRC_PATH: Path = ROOT_PATH / 'src'
""" The source path of the application which is typically the src directory within the ROOT_PATH. """

TEMPLATE_PATH: Path = SRC_PATH / 'templates'
""" The template path of the application which is typically the templates directory within the SRC_PATH. """


class AppSettings(BaseSettings):
    """ The application settings object that loads setting values from the application environment. """

    version: str = '0.1.0'
    """ The application version number """

    account_authentication_method: str = 'username_email'  # email, username, username_email
    account_email_required: bool = False
    account_email_verification: str = 'none'  # none, optional, required
    account_username_required: bool = False
    admin_email: str = 'admin@yourdomain.com'
    admin_from_email: str = 'noreply@yourdomain.com'
    admin_name: str = 'Admin'
    allowed_hosts: list[str] = ['*']
    anymail_amazon_ses_auto_confirm_sns_subscriptions: bool = True
    anymail_amazon_ses_client_params: dict = {}
    anymail_amazon_ses_configuration_set_name: str | None = None
    anymail_amazon_ses_message_tag_name: str | None = None
    anymail_amazon_ses_session_params: dict = {}
    anymail_mailersend_api_token: str | None = None
    anymail_mailersend_api_url: str = 'https://api.mailersend.com/v1'
    anymail_mailersend_batch_send_mode: str | None = None
    anymail_mailersend_inbound_secret: str | None = None
    anymail_mailersend_signing_secret: str | None = None
    anymail_mailgun_api_key: str | None = None
    anymail_mailgun_api_url: str = 'https://api.mailgun.net/v3'
    anymail_mailgun_sender_domain: str | None = None
    anymail_mailgun_webhook_signing_key: str | None = None
    anymail_mailjet_api_key: str | None = None
    anymail_mailjet_api_url: str = 'https://api.mailjet.com/v3'
    anymail_mailjet_secret_key: str | None = None
    anymail_mandrill_api_key: str | None = None
    anymail_mandrill_api_url: str = 'https://mandrillapp.com/api/1.0'
    anymail_mandrill_webhook_key: str | None = None
    anymail_mandrill_webhook_url: str | None = None
    anymail_postal_api_key: str | None = None
    anymail_postal_api_url: str | None = None
    anymail_postal_webhook_key: str | None = None
    anymail_postmark_api_url: str = 'https://api.postmarkapp.com/'
    anymail_postmark_server_token: str | None = None
    anymail_sendgrid_api_key: str | None = None
    anymail_sendgrid_api_url: str = 'https://api.sendgrid.com/v3/'
    anymail_sendgrid_generate_message_id: bool = True
    anymail_sendgrid_merge_field_format: str | None = None
    anymail_sendinblue_api_key: str | None = None
    anymail_sendinblue_api_url: str = 'https://api.sendinblue.com/v3/'
    anymail_sparkpost_api_key: str | None = None
    anymail_sparkpost_api_url: str = 'https://api.sparkpost.com/api/v1'
    anymail_sparkpost_subaccount: str | None = None
    anymail_sparkpost_track_initial_open_as_opened: bool = False
    config_path: str = '/etc/pda/config.yml'
    csrf_cookie_secure: bool = True
    debug: bool = False
    db_engine: str = 'sqlite'  # mysql, postgresql, sqlite
    db_host: str | None = None
    db_name: str | None = None
    db_password: str | None = None
    db_path: str | None = '/var/lib/pda/pda.db'
    db_port: int = 0
    db_url: str | None = None
    db_user: str | None = None
    email_backend: str | None = None
    email_host: str = 'localhost'
    email_host_user: str | None = None
    email_host_password: str | None = None
    email_port: int = 587
    email_ssl_certfile: str | None = None
    email_ssl_keyfile: str | None = None
    email_subject_prefix: str | None = '[PDA] '
    email_timeout: int = 0
    email_use_ssl: bool = False
    email_use_tls: bool = True
    env_type: str | None = 'production'  # development, production
    google_analytics_id: str | None = None
    language_code: str = 'en-us'
    language_cookie_name: str = 'pdns_admin_language'
    log_level_app: str = 'INFO'
    log_level_django: str = 'INFO'
    log_path: str = '/var/log/pda/pda.log'
    log_retention: int = 30
    log_rotation: str = 'daily'  # daily, weekly, monthly
    log_size: int = 10000000
    log_to_file: bool = False
    log_to_sentry: bool = False
    log_to_stdout: bool = True
    log_to_syslog: bool = False
    redis_host: str = ''
    redis_password: str | None = None
    redis_port: int = 6379
    redis_url: str = ''
    root_path: str = str(ROOT_PATH)
    secret_key: str = 'INSECURE-CHANGE-ME-6up8zksTD6mi4N3z3zFk'
    secure_hsts_include_subdomains: bool = True
    secure_hsts_preload: bool = True
    secure_hsts_seconds: int | str | None = 2592000
    secure_proxy_ssl_header_name: str = 'HTTP_X_FORWARDED_PROTO'
    secure_proxy_ssl_header_value: str = 'https'
    secure_ssl_redirect: bool = True
    sentry_dsn: str = ''
    server_address: str = '0.0.0.0'
    server_port: int = 8080
    session_cookie_secure: bool = True
    site_description: str = 'A PowerDNS web interface with advanced features.'
    site_email: str = 'pda@yourdomain.com'
    site_from_email: str = 'pda@yourdomain.com'
    site_logo: str | None = None
    site_title: str = 'PowerDNS Admin'
    site_url: str = 'https://pda.yourdomain.com'
    src_path: str = str(SRC_PATH)
    syslog_host: str | None = None
    syslog_port: int = 514
    template_path: str = str(TEMPLATE_PATH)
    time_zone: str = 'UTC'
    use_https_in_absolute_urls: bool = True
    use_i18n: bool = True
    use_l10n: bool = True
    use_tz: bool = True

    """ The following settings are automatically loaded at application startup. """

    config: dict | None = None
    """ Additional configuration settings loaded automatically from the given YAML configuration file (if any) """

    class Config:
        env_prefix = 'pda_'


def load_settings(env_file_path: str = '.env', env_file_encoding: str = 'UTF-8',
                  secrets_path: str | None = None) -> AppSettings:
    """ Loads an AppSettings instance based on the given environment file and secrets directory. """

    params: dict = {
        '_env_file': env_file_path,
        '_env_file_encoding': env_file_encoding,
    }

    os.putenv('PDA_ENV_FILE', env_file_path)
    os.putenv('PDA_ENV_FILE_ENCODING', env_file_encoding)

    if secrets_path is not None:
        valid: bool = True

        if not os.path.exists(secrets_path):
            valid = False
            print(f'The given path for the "--secrets-dir" option does not exist: {secrets_path}')
        elif not os.path.isdir(secrets_path):
            valid = False
            print(f'The given path for the "--secrets-dir" option is not a directory: {secrets_path}')

        if valid:
            params['_secrets_dir'] = secrets_path
            os.putenv('PDA_ENV_SECRETS_DIR', secrets_path)

    # Load base app configuration settings from the given environment file and the local environment
    app_settings = AppSettings(**params)

    # Load additional configuration from the given YAML configuration file (if any)
    if app_settings.config_path is not None:
        if not app_settings.config_path.startswith('/'):
            app_settings.config_path = os.path.join(app_settings.root_path, app_settings.config_path)
        app_settings = load_config(app_settings)

    # Prepend the root path to the database path if it is not an absolute path
    if isinstance(app_settings.db_path, str) and len(
            app_settings.db_path.strip()) and not app_settings.db_path.startswith('/'):
        app_settings.db_path = str(os.path.join(app_settings.root_path, app_settings.db_path))

    return app_settings


def load_config(app_settings: AppSettings) -> AppSettings:
    """ Loads the app's configuration from the given configuration file. """
    from yaml import YAMLError

    config_path: str | None = app_settings.config_path

    if not isinstance(config_path, str):
        return app_settings

    if len(config_path.strip()) == 0:
        return app_settings

    if not config_path.startswith('/'):
        config_path = os.path.join(app_settings.root_path, config_path)

    try:
        with open(config_path, 'r') as f:
            app_settings.config = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
    except FileNotFoundError:
        # print(f'The given path for the configuration file does not exist: {config_path}')
        pass
    except IsADirectoryError:
        # print(f'The given path for the configuration file is not a file: {config_path}')
        pass
    except PermissionError:
        # print(f'Permission denied when trying to read the configuration file: {config_path}')
        pass
    except UnicodeDecodeError:
        # print(f'Failed to decode the configuration file: {config_path}')
        pass
    except YAMLError as e:
        # print(f'Failed to parse the configuration file "{config_path}": {e}')
        pass

    return app_settings


def save_config(app_settings: AppSettings, config: dict[str, any]) -> bool:
    """ Saves the app's configuration to the defined configuration file setting path. """

    config_path: str = app_settings.config_path

    if not config_path.startswith('/'):
        config_path = os.path.join(app_settings.root_path, config_path)

    with open(config_path, 'w') as f:
        yaml.dump(config, f)
        f.close()

    return True


# Define the default environment file path to load settings from
env_conf_path: str = os.getenv('PDA_ENV_FILE', str(ROOT_PATH / '.env'))

# Load various Django settings from an environment file and the local environment
settings: AppSettings = load_settings(env_conf_path)
