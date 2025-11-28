from app.lib.config.app import AppConfig
from app.lib.config.api import ApiConfig
from app.lib.config.celery import CeleryConfig
from app.lib.config.db import DbConfig
from app.lib.config.logging import LoggingConfig
from app.lib.config.mail import MailConfig
from app.lib.config.notifications import NotificationsConfig
from app.lib.config.paths import PathsConfig
from app.lib.config.server import ServerConfig
from app.lib.config.services import ServicesConfig
from app.lib.config.tasks import TasksConfig
from app.models.base import BaseConfig


class Config(BaseConfig):
    """A model that represents the root level element of the app configuration hierarchy."""

    api: ApiConfig
    app: AppConfig
    celery: CeleryConfig
    db: DbConfig
    logging: LoggingConfig
    mail: MailConfig
    notifications: NotificationsConfig
    paths: PathsConfig
    server: ServerConfig
    services: ServicesConfig
    tasks: TasksConfig
