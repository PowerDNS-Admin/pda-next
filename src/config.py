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
    admin_email: str = 'admin@yourdomain.com'
    admin_from_email: str = 'noreply@yourdomain.com'
    admin_name: str = 'Admin'
    allowed_hosts: list[str] = ['*']
    config_path: str = '/etc/pda/config.yml'
    csrf_cookie_secure: bool = True
    debug: bool = False
    dev_server_address: str = '0.0.0.0'
    dev_server_port: int = 8080
    django_log_level: str = 'INFO'
    db_engine: str = 'sqlite'  # mysql, postgresql, sqlite
    db_host: str | None = None
    db_name: str | None = None
    db_password: str | None = None
    db_path: str = '/var/lib/pda/pda.db'
    db_port: int | None = None
    db_url: str = 'sqlite:///pda.db'
    db_user: str | None = None
    email_backend: str | None = None
    email_host: str = 'localhost'
    email_host_user: str | None = None
    email_host_password: str | None = None
    email_port: int = 587
    email_ssl_certfile: str | None = None
    email_ssl_keyfile: str | None = None
    email_subject_prefix: str | None = '[PDA] '
    email_timeout: int | None = None
    email_use_ssl: bool = False
    email_use_tls: bool = True
    google_analytics_id: str | None = None
    language_code: str = 'en-us'
    language_cookie_name: str = 'pdns_admin_language'
    log_level: str = 'INFO'
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
    session_cookie_secure: bool = True
    site_description: str = 'PowerDNS Admin is a web interface for PowerDNS'
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

    config_path: str | None = app_settings.config_path

    if not isinstance(config_path, str):
        return app_settings

    if not config_path.startswith('/'):
        config_path = os.path.join(app_settings.root_path, config_path)

    if not os.path.exists(config_path):
        raise Exception(f'The given path for the configuration file does not exist: {config_path}')

    if not os.path.isfile(config_path):
        raise Exception(f'The given path for the configuration file is not a file: {config_path}')

    with open(config_path, 'r') as f:
        app_settings.config = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

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
