from lib.config.app import AppConfig
from lib.config.api import ApiConfig
from lib.config.celery import CeleryConfig
from lib.config.db import DbConfig
from lib.config.logging import LoggingConfig
from lib.config.mail import MailConfig
from lib.config.notifications import NotificationsConfig
from lib.config.paths import PathsConfig
from lib.config.server import ServerConfig
from lib.config.services import ServicesConfig
from lib.config.tasks import TasksConfig
from models import BaseConfig


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
