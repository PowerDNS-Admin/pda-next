from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader, select_autoescape
from redis.asyncio import Redis
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

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
db_engine_sync = Optional[Engine]
AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None
SessionLocal: Optional[sessionmaker[Session]] = None
redis: Optional[Redis] = None
mysql: Optional[MysqlClient] = None
zabbix: Optional[ZabbixReporter] = None


def app_startup(use_sync: bool = False):
    """Executes appropriate app startup tasks."""
    from lib import load_environment, load_settings, init_logging, init_redis
    from lib.jinja import JinjaFilters

    global settings, config, notifications, schedules, redis, db_engine, db_engine_sync, AsyncSessionLocal, \
        SessionLocal, j2, zabbix

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

    # Initialize Redis connection
    redis = init_redis(config=config)

    # Initialize SQL connection
    db_engine = create_async_engine(
        config.db.sql_async_url,
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

    if use_sync:
        db_engine_sync = create_engine(
            config.db.sql_sync_url,
            echo=False,
            future=True,
            pool_pre_ping=True,
        )

        SessionLocal = sessionmaker(
            bind=db_engine_sync,
            class_=Session,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

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


async def app_shutdown(use_sync: bool = False):
    """Executes appropriate app shutdown tasks."""
    global db_engine, db_engine_sync, redis, zabbix

    # Dispose of SQL connection pool
    await db_engine.dispose()

    if use_sync:
        db_engine_sync.dispose()

    # Dispose of Redis connection pool
    await redis.close()

    # Stop Zabbix Reporter worker
    await zabbix.stop_async()


STARTUP_TASKS = []
RUNNING_TASKS = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    from routers import install_routers

    config = app_startup()

    # Initialize all tasks defined in STARTUP_TASKS list
    for task in STARTUP_TASKS:
        RUNNING_TASKS.append(asyncio.create_task(task()))

    # Set up FastAPI routers
    install_routers(app, config)

    yield

    # Cancel all tasks defined in the RUNNING_TASKS list
    for task in RUNNING_TASKS:
        task.cancel()

    await app_shutdown()
