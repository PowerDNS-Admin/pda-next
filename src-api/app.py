from __future__ import annotations
from jinja2 import Environment, FileSystemLoader, select_autoescape
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from typing import Optional
from lib import AppSettings
from lib.config import Config
from lib.config.app import AppConfig
from lib.config.tasks import TaskSchedule
from lib.mysql import MysqlClient
from lib.notifications.config import NotificationConfig
from lib.services.zabbix import ZabbixReporter

INIT_INTERVAL_DEFAULT = 300
INIT_INTERVAL_THRESHOLD = 0.5
INIT_DB_INTERVAL_DEFAULT = 300
INIT_DB_INTERVAL_THRESHOLD = 0.5

settings: Optional[AppSettings] = None
config: Optional[Config] = None
notifications: Optional[list[NotificationConfig]] = None
schedules: Optional[list[TaskSchedule]] = None
j2: Optional[Environment] = None
db_engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None
redis: Optional[Redis] = None
mysql: Optional[MysqlClient] = None
zabbix: Optional[ZabbixReporter] = None


def initialize():
    from lib import load_environment, load_settings, init_logging, init_mysql, init_redis
    from lib.jinja import JinjaFilters

    global settings, config, notifications, schedules, j2, mysql, redis, zabbix, db_engine, AsyncSessionLocal

    # Initialize logging configuration with defaults
    init_logging()

    # Get the environment variable prefix from the default configuration
    env_prefix = AppConfig.EnvironmentConfig.model_fields['prefix'].default

    # Load the environment settings from the file system
    load_environment(env_prefix)

    # Load the application settings model based on default environment settings
    settings = load_settings(env_prefix=env_prefix)
    # Reload the application settings model based on prefix loaded from the environment if different from the default
    if settings.env_prefix != env_prefix:
        settings = load_settings(env_prefix=settings.env_prefix)

    # Load app configuration into a statically typed object mimicking the hierarchy
    config = settings.config

    # Load app notifications configuration
    notifications = settings.notifications

    # Load app scheduling configuration
    schedules = settings.schedules

    # Re-initialize logging configuration with loaded environment and configuration settings
    init_logging(config=config, settings=settings)

    # Close existing MySQL connection
    if isinstance(mysql, MysqlClient):
        try:
            mysql.disconnect()
        except Exception:
            pass

    # Initialize SQL connection
    db_engine = create_async_engine(
        config.db.sql_url,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )

    AsyncSessionLocal = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    # Initialize MySQL connection
    mysql = init_mysql(config=config)

    # Close existing Redis connection
    if redis:
        try:
            redis.close()
        except Exception:
            pass

    # Initialize Redis connection
    redis = init_redis(config=config)

    # Set up Jinja2 template rendering
    j2 = Environment(
        loader=FileSystemLoader(config.paths.templates),
        autoescape=select_autoescape(),
    )

    j2.globals['settings'] = settings
    j2.globals['config'] = config
    j2.filters = JinjaFilters.implement_filters(j2.filters)

    # Initialize Zabbix Reporter
    zabbix = ZabbixReporter(config=config.services.zabbix)
    zabbix.start()

    return config


async def init_loop():
    import asyncio
    from loguru import logger
    from lib import load_config

    global config

    first_run = True
    interval = INIT_INTERVAL_DEFAULT

    while True:
        try:
            updated_config = load_config()

            repeat = updated_config.api.runtime.init.repeat
            interval = updated_config.api.runtime.init.repeat_interval

            if not repeat:
                interval = updated_config.api.runtime.init.repeat_recovery_interval

            if interval < INIT_INTERVAL_THRESHOLD:
                interval = INIT_INTERVAL_THRESHOLD

            if not first_run and repeat:
                config = initialize()
                logger.trace('Application reinitialized.')

        except Exception as e:
            logger.error(f'Failed to reinitialize application: {e}')

        logger.trace(f'Waiting {interval} seconds until next app reinitialization cycle.')

        await asyncio.sleep(interval)

        first_run = False


async def init_db_loop():
    import asyncio
    from loguru import logger
    from lib import init_db_schema, load_config

    global config

    first_run = True
    interval = INIT_DB_INTERVAL_DEFAULT

    while True:
        try:
            updated_config = load_config()

            enabled = updated_config.api.runtime.init.init_db
            repeat = updated_config.api.runtime.init.repeat_db
            interval = updated_config.api.runtime.init.repeat_db_interval

            if not repeat:
                interval = updated_config.api.runtime.init.repeat_db_recovery_interval

            if interval < INIT_DB_INTERVAL_THRESHOLD:
                interval = INIT_DB_INTERVAL_THRESHOLD

            if (enabled and first_run and not repeat) or (enabled and repeat and not first_run):
                init_db_schema(config)
                logger.trace('Database reinitialized.')

        except Exception as e:
            logger.error(f'Failed to initialize database schema: {e}')

        logger.trace(f'Waiting {interval} seconds until next db reinitialization cycle.')

        await asyncio.sleep(interval)

        first_run = False
