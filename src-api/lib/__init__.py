import logging
import os
import sys
from loguru import logger
from pathlib import Path
from pydantic_settings import BaseSettings
from redis.asyncio.client import Redis
from typing import Union
from lib.config import Config
from lib.config.app import AppConfig
from lib.config.tasks import TaskSchedule
from lib.mysql import MysqlClient
from lib.notifications.config import NotificationConfig
from lib.util.config import ConfigLoader

ROOT_PATH: Path = Path(os.getcwd())
""" The root path of the application which is typically the project repository root directory."""

DEFAULT_ENV_NAME: str = AppConfig.EnvironmentConfig.model_fields['name'].default
""" The default environment name to use for initialization. """


class AppSettings(BaseSettings):
    """ The application settings class that loads setting values from the application environment. """

    _config: Config = None
    """The cached configuration data loaded from YAML."""

    config_path: Union[str, Path] = 'config/config.yml'
    """ The path to the YAML file containing additional configuration settings. """

    debug: bool = False
    """ Whether debug mode is enabled. """

    env: str = DEFAULT_ENV_NAME
    """ The name of the environment. """

    env_file: Union[str, Path, None] = AppConfig.EnvironmentConfig.model_fields['file'].default
    """ The path to the environment file to load settings from. """

    env_file_encoding: str = 'UTF-8'
    """ The file encoding of the environment file to load settings from. """

    env_prefix: str = AppConfig.EnvironmentConfig.model_fields['prefix'].default
    """ The prefix of the environment settings variables to load from the environment. """

    env_secrets_dir: Union[str, Path, None] = None
    """ The path to the secrets directory to load environment variable values from. """

    notification_path: Union[str, Path] = 'config/notifications.yml'
    """ The path to the YAML file containing notifications configuration data. """

    root_path: Union[str, Path] = Path(os.getcwd())
    """ The root path of the application which is typically the project repository root directory. """

    schedule_path: Union[str, Path] = 'config/schedules.yml'
    """ The path to the YAML file containing task scheduling data. """

    version: str = AppConfig.model_fields['version'].default
    """ The application version number """

    @property
    def config(self) -> Config:
        """ Returns a configuration data provided by the YAML file given in the config_path setting (if any). """
        if isinstance(self._config, Config):
            return self._config

        default_config = Config(**{})

        if not self.config_path:
            return default_config

        config_path = Path(self.config_path)

        if not config_path.exists():
            return default_config

        loaded_config = ConfigLoader.load_yaml(self.config_path)

        if loaded_config is None:
            return default_config

        self._config = Config(**loaded_config)

        return self._config

    @property
    def notifications(self) -> Union[list[NotificationConfig], None]:
        """
        Returns the notifications configuration data provided by the YAML file given in the notification_path
        setting (if any).
        """
        from lib.util.config import ConfigUtil

        if not Path(self.notification_path).exists():
            return None

        loaded_config = ConfigLoader.load_yaml(self.notification_path)

        if loaded_config is None:
            return None

        if isinstance(loaded_config, list):
            return [NotificationConfig(**c) for c in loaded_config]

        return [NotificationConfig(**loaded_config)]

    @property
    def schedules(self) -> Union[list[TaskSchedule], None]:
        """
        Returns the task scheduling data provided by the YAML file given in the schedule_path setting (if any).
        """
        from lib.util.config import ConfigUtil

        if not Path(self.schedule_path).exists():
            return None

        loaded_config = ConfigLoader.load_yaml(self.schedule_path)

        if loaded_config is None:
            return None

        return [TaskSchedule(**c) for c in loaded_config]

    class Config:
        env_prefix = AppConfig.EnvironmentConfig.model_fields['prefix'].default + '_'
        env_nested_delimiter = '__'


DEFAULT_ENV_PATH: Path = ROOT_PATH / AppSettings.model_fields['env_file'].default
""" The default path to the environment file to load settings from. """

DEFAULT_ENV_FILE_ENCODING: str = AppSettings.model_fields['env_file_encoding'].default
""" The default file encoding of the environment file to load settings from. """

DEFAULT_SECRETS_PATH: Union[Path, None] = AppSettings.model_fields['env_secrets_dir'].default
""" The default path to the secrets directory to load environment variable values from. """


def load_environment(env_prefix: str):
    """ Loads available environment files based on current environment. """
    from dotenv import load_dotenv
    from loguru import logger

    env_name = os.getenv(f'{env_prefix}_ENV', DEFAULT_ENV_NAME).lower()

    logger.trace(f'Loading environment file for environment: {env_name}; prefix: {env_prefix};)')

    env_paths = ['.app.env', f'.app.{env_name}.env']

    for file_path in env_paths:
        if (env_path := ROOT_PATH / file_path).exists():
            logger.trace(f'Loading environment file: {env_path}')
            load_dotenv(env_path)


def load_settings(env_prefix: str) -> AppSettings:
    """ Loads an AppSettings instance based on the given environment file and secrets directory. """
    from loguru import logger

    # Extract the default environment file path from the environment if defined, otherwise use the default path
    env_file_path = os.getenv(f'{env_prefix}_ENV_FILE', DEFAULT_ENV_PATH)

    # Extract the default environment file encoding from the environment if defined, otherwise use the default value
    env_file_encoding = os.getenv(f'{env_prefix}_ENV_FILE_ENCODING', DEFAULT_ENV_FILE_ENCODING)

    # Extract the default secrets directory path from the environment if defined, otherwise use the default path
    secrets_path = os.getenv(f'{env_prefix}_ENV_SECRETS_DIR', DEFAULT_SECRETS_PATH)

    if env_file_path is not None and not isinstance(env_file_path, Path):
        env_file_path = Path(env_file_path)

    if secrets_path is not None and not isinstance(secrets_path, Path):
        secrets_path = Path(secrets_path)

    params: dict = {
        'root_path': str(ROOT_PATH),
        'env_file': str(env_file_path),
        'env_file_encoding': env_file_encoding,
        '_env_file': env_file_path,
        '_env_file_encoding': env_file_encoding,
    }

    # Ensure any default values get pushed back into the environment
    os.putenv(f'{env_prefix}_ENV_FILE', str(env_file_path))
    os.putenv(f'{env_prefix}_ENV_FILE_ENCODING', env_file_encoding)

    if secrets_path is not None:
        valid: bool = True

        if not secrets_path.exists():
            valid = False
            logger.warning(f'The given path for the "--secrets-dir" option does not exist: {secrets_path}')
        elif not secrets_path.is_dir():
            valid = False
            logger.warning(f'The given path for the "--secrets-dir" option is not a directory: {secrets_path}')

        if valid:
            params['secrets_dir'] = secrets_path
            # Ensure the default value gets pushed back into the environment
            os.putenv(f'{env_prefix}_ENV_SECRETS_DIR', str(secrets_path))

    return AppSettings(**params)


def load_config() -> Config:
    # Get the environment variable prefix from the default configuration
    env_prefix = AppConfig.EnvironmentConfig.model_fields['prefix'].default
    # Load the app settings from the environment
    settings = load_settings(env_prefix=env_prefix)
    # Reload the application settings model based on prefix loaded from the environment if different from the default
    if settings.env_prefix != env_prefix:
        settings = load_settings(env_prefix=settings.env_prefix)
    # Load app configuration
    return settings.config


def load_notifications() -> list[NotificationConfig]:
    # Get the environment variable prefix from the default configuration
    env_prefix = AppConfig.EnvironmentConfig.model_fields['prefix'].default
    # Load the app settings from the environment
    settings = load_settings(env_prefix=env_prefix)
    # Reload the application settings model based on prefix loaded from the environment if different from the default
    if settings.env_prefix != env_prefix:
        settings = load_settings(env_prefix=settings.env_prefix)
    # Load app configuration
    return settings.notifications if settings.notifications else []


def load_schedules() -> list[TaskSchedule]:
    # Get the environment variable prefix from the default configuration
    env_prefix = AppConfig.EnvironmentConfig.model_fields['prefix'].default
    # Load the app settings from the environment
    settings = load_settings(env_prefix=env_prefix)
    # Reload the application settings model based on prefix loaded from the environment if different from the default
    if settings.env_prefix != env_prefix:
        settings = load_settings(env_prefix=settings.env_prefix)
    # Load app configuration
    return settings.schedules if settings.schedules else []


def init_logging(config: Config = None, settings: AppSettings = None) -> None:
    """
    Initialize logging configuration
    """
    from lib.config import Config

    log_format: str = '<green>{time}</green> <level>{level}</level>'
    log_level: str = 'INFO'

    if isinstance(settings, AppSettings):
        if settings.debug:
            log_level = 'DEBUG'
        if config is None:
            config = settings.config

    if isinstance(config, Config) and config.logging.level is not None:
        log_level = config.logging.level.upper()

    if log_level.lower() in ['debug', 'trace', 'trace1', 'trace2', 'trace3', 'trace4', 'trace5']:
        log_format += ' <cyan>{module}.{name}:{function}:{line}</cyan>'

    log_format += ' <level>{message}</level>'
    logger.remove()
    logger.add(sys.stderr, colorize=True, format=log_format, level=log_level)

    logging.getLogger('pydantic').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def init_mysql(config: Config) -> MysqlClient:
    """ Initialize a MySQL database connection. """
    from lib.mysql import MysqlClient, MysqlDbConfig
    return MysqlClient(
        MysqlDbConfig(**config.db.mysql.model_dump()),
        auto_connect=False, pool_recycle=3600, pool_pre_ping=True
    )


def init_redis(config: Config) -> Redis:
    """ Initialize a Redis connection instance. """
    return Redis.from_url(
        url=f'redis://{config.db.redis.host}:{config.db.redis.port}/{config.db.redis.database}',
        decode_responses=True,
        pool_timeout=5,
    )


def init_db_schema(config: Config):
    """
    Initialize the application database
    :return: None
    """
    from loguru import logger
    from lib.mysql import MysqlClient, MysqlDbConfig
    engine_opts = {
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    logger.debug('Initializing database schema...')
    MysqlClient(MysqlDbConfig(**config.db.mysql.model_dump()), **engine_opts).create_schema()
    logger.debug('Database schema initialized.')
