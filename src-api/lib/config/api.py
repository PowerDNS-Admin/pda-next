from models.base import BaseConfig


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
                    self.ApiMetadataTagConfig(name='default',
                                              description='Provides browser client entrypoint and monitoring functionality.'),
                    self.ApiMetadataTagConfig(name='tasks',
                                              description='Provides task execution and monitoring features'),
                ]

    metadata: ApiMetadataConfig
    runtime: ApiRuntimeConfig
