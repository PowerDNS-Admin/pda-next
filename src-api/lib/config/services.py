from typing import Optional
from models import BaseConfig


class ServicesConfig(BaseConfig):
    """A model that represents a configuration hierarchy for external service integrations."""

    class TwilioConfig(BaseConfig):
        """Provides Twilio service configuration."""

        class TwilioApiConfig(BaseConfig):
            """Provides Twilio API configurations for the live and test environments."""

            class TwilioApiEnvironmentConfig(BaseConfig):
                """Provides Twilio API configuration for a specific environment."""
                account_sid: str
                auth_token: str

            live: TwilioApiEnvironmentConfig
            test: TwilioApiEnvironmentConfig

        class TwilioNumberConfig(BaseConfig):
            """Provides Twilio account number configuration."""
            sid: str
            number: str
            voice: bool = False
            sms: bool = False
            mms: bool = False
            faxes: bool = False

        api: TwilioApiConfig
        numbers: list[TwilioNumberConfig]

    class ZabbixConfig(BaseConfig):
        hostname: str = 'zabbix'
        port: int = 10051
        send_interval: float = 1
        default_node_name: str = 'pda'
        reporter_enabled: bool = True
        sender_enabled: bool = True

    twilio: Optional[TwilioConfig] = None
    zabbix: ZabbixConfig
