from typing import Optional
from models.base import BaseConfig


class MailConfig(BaseConfig):
    """A model that represents a configuration hierarchy for email features."""

    class MailServer(BaseConfig):
        class MailServerThrottle(BaseConfig):
            threshold: int = 5
            period: float = 30
            mode: str = 'sleep' # sleep or raise
            key: Optional[str] = None
            backoff_strategy: str = 'fixed' # fixed or exponential
            backoff_base: float = 1.0
            backoff_cap: float = 60.0
            jitter: bool = False

        alias: str
        host: str
        port: int = 25
        tls: bool = False
        ssl: bool = False
        local_hostname: Optional[str] = None
        source_address: Optional[tuple] = None
        timeout: Optional[int] = 60
        key_file: Optional[str] = None
        cert_file: Optional[str] = None
        username: Optional[str] = None
        password: Optional[str] = None
        from_address: Optional[str] = None
        throttle: MailServerThrottle

    servers: Optional[list[MailServer]] = None
