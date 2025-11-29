from models import BaseConfig


class CeleryConfig(BaseConfig):
    """A model that represents a configuration hierarchy for the Celery app."""

    class BrokerConfig(BaseConfig):
        url: str = 'redis://redis:6379/0'

    class BackendConfig(BaseConfig):
        url: str = 'redis://redis:6379/0'

    broker: BrokerConfig
    backend: BackendConfig
