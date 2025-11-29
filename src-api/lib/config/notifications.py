from models import BaseConfig


class NotificationsConfig(BaseConfig):
    """A model that represents a configuration hierarchy for notification settings."""

    class NotificationServiceConfig(BaseConfig):
        """Provides an abstract class for notification services to inherent from."""
        enabled: bool = False

    mail: NotificationServiceConfig
    microsoft_teams: NotificationServiceConfig
    twilio: NotificationServiceConfig
