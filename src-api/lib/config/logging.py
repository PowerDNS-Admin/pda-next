from models.base import BaseConfig


class LoggingConfig(BaseConfig):
    """A model that represents a configuration hierarchy for logging settings."""
    level: str = 'info'
