import os
import yaml
from pathlib import Path
from pydantic import BaseSettings

ROOT_PATH: Path = Path(__file__).parent.parent
SRC_PATH: Path = ROOT_PATH / 'src'
TEMPLATE_PATH: Path = SRC_PATH / 'templates'


class AppSettings(BaseSettings):
    version: str = '0.1.0'

    site_title: str = 'PowerDNS Admin'
    site_description: str = 'PowerDNS Admin is a web interface for PowerDNS'
    site_url: str = 'https://demo.powerdnsadmin.org'
    site_logo: str = 'https://demo.powerdnsadmin.org/static/img/logo.png'
    site_email: str = 'admin@powerdnsadmin.org'
    site_from_email: str = 'pda@powerdnsadmin.org'
    admin_name: str = 'Admin'
    admin_email: str = 'admin@yourdomain.com'
    admin_from_email: str = 'noreply@yourdomain.com'
    root_path: str = str(ROOT_PATH)
    src_path: str = str(SRC_PATH)
    template_path: str = str(TEMPLATE_PATH)
    config_path: str = '/etc/pda/config.yml'
    allowed_hosts: list[str] = ['*']
    secure_proxy_ssl_header_name: str = 'HTTP_X_FORWARDED_PROTO'
    secure_proxy_ssl_header_value: str = 'https'
    secure_ssl_redirect: bool = True
    session_cookie_secure: bool = True
    csrf_cookie_secure: bool = True
    secure_hsts_seconds: int | str | None = 2592000
    """ HSTS (HTTP Strict Transport Security) Seconds (30 days in seconds)"""
    secure_hsts_include_subdomains: bool = True
    secure_hsts_preload: bool = True
    debug: bool = False
    dev_server_address: str = '0.0.0.0'
    dev_server_port: int = 8080
    django_log_level: str = 'INFO'
    log_level: str = 'INFO'
    secret_key: str = 'INSECURE-CHANGE-ME-6up8zksTD6mi4N3z3zFk'
    db_url: str = 'sqlite:///pda.db'
    db_engine: str = 'sqlite'  # mysql, postgresql, sqlite
    db_path: str = '/var/lib/pda/pda.db'
    db_host: str = ''
    db_port: int | None = None
    db_user: str = ''
    db_password: str = ''
    db_name: str = ''
    redis_url: str = ''
    redis_host: str = ''
    redis_port: int = 6379
    time_zone: str = 'UTC'
    use_i18n: bool = True
    use_l10n: bool = True
    use_tz: bool = True
    use_https_in_absolute_urls: bool = True
    language_code: str = 'en-us'
    language_cookie_name: str = 'pdns_admin_language'
    email_backend: str | None = None
    account_email_required: bool = False
    account_email_verification: str = 'none'  # none, optional, required
    account_authentication_method: str = 'username_email'  # email, username, username_email
    google_analytics_id: str = ''
    sentry_dsn: str = ''

    config: dict | None = None
    """ Additional configuration settings loaded from the given YAML configuration file (if any) """

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
