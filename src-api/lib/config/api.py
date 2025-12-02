from models import BaseConfig


class ApiConfig(BaseConfig):
    """A model that represents a configuration hierarchy for the FastAPI app."""

    class ApiRuntimeConfig(BaseConfig):
        class ApiRuntimeInitConfig(BaseConfig):
            repeat: bool = False
            repeat_interval: float = 300
            repeat_recovery_interval: float = 300
            init_db: bool = False
            repeat_db: bool = False
            repeat_db_interval: float = 300
            repeat_db_recovery_interval: float = 300

        init: ApiRuntimeInitConfig

    class ApiMetadataConfig(BaseConfig):
        class ApiMetadataTagConfig(BaseConfig):
            name: str
            description: str

        tags: list[ApiMetadataTagConfig] = []

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if not self.tags:
                self.tags = [
                    self.ApiMetadataTagConfig(
                        name='default',
                        description='Provides browser client entrypoint and monitoring functionality.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='auth',
                        description='Provides functionality for managing, monitoring, and authenticating users and OAuth clients.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='acl',
                        description='Provides functionality for managing permissions for users and OAuth clients.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='settings',
                        description='Provides functionality for managing system, tenant, and user level settings.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='system',
                        description='Provides functionality for managing system resources.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='tenants',
                        description='Provides functionality for managing system tenants.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='servers',
                        description='Provides functionality for managing DNS servers and settings.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='keys',
                        description='Provides features for managing DNS keys.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='zones',
                        description='Provides functionality for managing DNS zones and records.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='views',
                        description='Provides functionality for managing DNS views and related resources.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='tasks',
                        description='Provides functionality for managing and monitoring task execution.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='services',
                        description='Provides access to various system service features.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='dev',
                        description='Provides development mode resources and tools.',
                    ),
                ]

    metadata: ApiMetadataConfig
    runtime: ApiRuntimeConfig
