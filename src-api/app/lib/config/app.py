from app.models.base import BaseConfig


class AppConfig(BaseConfig):
    """A model that represents a configuration hierarchy shared across descendant apps."""

    class AuthorConfig(BaseConfig):
        name: str = 'PowerDNS Admin'
        email: str = 'admin@powerdnsadmin.org'
        url: str = 'https://powerdnsadmin.org'

    class EnvironmentConfig(BaseConfig):
        class EnvironmentUrlsConfig(BaseConfig):
            api: str = None
            web: str = None

        name: str = 'prod'
        prefix: str = 'PDA'
        file: str = 'config/.app.env'
        urls: EnvironmentUrlsConfig

    class MetadataConfig(BaseConfig):
        description: str = '''The PDA API provides a backend interface for core functionality and support of the UI.'''

    name: str = 'pda'
    version: str = '0.1.0'
    summary: str = 'A PowerDNS web interface with advanced management and automation features.'
    timezone: str = 'Etc/UTC'
    timezone_code: str = 'UTC'
    author: AuthorConfig
    environment: EnvironmentConfig
    metadata: MetadataConfig
