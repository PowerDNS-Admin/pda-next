from datetime import datetime
from typing import Optional, Union
from zoneinfo import ZoneInfo
from app.lib.enums import NotificationServiceEnum, TaskEnum
from app.lib.notifications.config import (
    ALL_SERVICE_RECIPIENTS_TYPE, ALL_NOTIFICATION_SERVICES_TYPE,
    NotificationConfig,
    MailNotificationService, MsTeamsNotificationService, TwilioNotificationService,
    MailServiceRecipient, MsTeamsServiceRecipient, TwilioServiceRecipient
)
from app.lib.notifications.events import ALL_EVENTS, ALL_EVENTS_TYPE

UTC_TZ = ZoneInfo('UTC')


class NotificationSender:
    """Provides an abstract interface for sending notifications."""

    SERVICE: NotificationServiceEnum
    """Defines the service name that this sender represents."""

    event: ALL_EVENTS
    """Defines the event to be used for this sender instance."""

    config: NotificationConfig
    """Defines the notification configuration to be used for this sender instance."""

    service: ALL_NOTIFICATION_SERVICES_TYPE
    """Defines the service configuration to be used for this sender instance."""

    def __init__(self, event: ALL_EVENTS, config: NotificationConfig, service: ALL_NOTIFICATION_SERVICES_TYPE):
        """Initializes a new instance of the notification sender class."""
        self.event = event
        self.config = config
        self.service = service

        if not self.config.enabled:
            raise ValueError(f'NotificationConfig provided to NotificationSender is disabled.')

        if not self.service.enabled:
            raise ValueError(f'NotificationService provided to NotificationSender is disabled.')

    def send(self, recipient: ALL_SERVICE_RECIPIENTS_TYPE):
        """Sends a notification to the given service recipient for the given event."""

        if not self.config.enabled:
            raise ValueError(f'NotificationConfig provided to NotificationSender is disabled.')

        if not self.service.enabled:
            raise ValueError(f'NotificationService provided to NotificationSender is disabled.')

        raise NotImplementedError()


class MailNotificationSender(NotificationSender):
    """Provides an API for sending mail notifications."""

    SERVICE: NotificationServiceEnum = NotificationServiceEnum.MAIL
    """Defines the service name that this sender represents."""

    service: MailNotificationService
    """Defines the service configuration to be used for this sender instance."""

    def send(self, recipient: MailServiceRecipient):
        """Sends a notification to the given service recipient for the given event."""
        from loguru import logger
        from worker import app as celery_app

        try:
            super().send(recipient)
        except NotImplementedError:
            pass

        mail_to = recipient.email

        if isinstance(recipient.name, str) and len(recipient.name.strip()):
            mail_to = f'{recipient.name} <{recipient.email}>'

        conf = {
            'mail_to': mail_to,
            'subject': self.event.message_subject,
            'template_path': 'pda/alert',
            'data': {
                'message_html': self.event.message_body_html,
                'message_plain': self.event.message_body_plain,
                'title': self.event.message_title,
            },
        }

        logger.debug(f'Sending notification email: Config: {self.config.label}, Recipient: {recipient.label}, '
                     + f'Category: {self.event.category}')

        celery_app.send_task(TaskEnum.PDA_MAIL_SEND.value, kwargs=conf)


class MsTeamsNotificationSender(NotificationSender):
    """Provides an API for sending mail notifications."""

    SERVICE: NotificationServiceEnum = NotificationServiceEnum.MSTEAMS
    """Defines the service name that this sender represents."""

    service: MsTeamsNotificationService
    """Defines the service configuration to be used for this sender instance."""

    def send(self, recipient: MsTeamsServiceRecipient):
        """Sends a notification to the given service recipient for the given event."""
        import json
        import requests
        from loguru import logger
        from app.lib.services.microsoft.adaptivecards import ContainerStyleEnum
        from app.lib.services.microsoft.teams import MessageFactory

        try:
            super().send(recipient)
        except NotImplementedError:
            pass

        headers = {'Content-Type': 'application/json'}

        payload = MessageFactory.create_simple_message(
            segments=self.event.message_body_plain.split('\n'),
            title=self.event.message_title,
            style=ContainerStyleEnum.attention,
        ).model_dump(mode='json', by_alias=True, exclude_none=True)

        response = requests.post(recipient.webhook, headers=headers, data=json.dumps(payload))

        if 200 <= response.status_code < 300:
            logger.debug(f'MicrosoftTeams: Successfully sent alert to Microsoft Teams webhook.')
        else:
            logger.error(f'MicrosoftTeams: Failed to send alert to Microsoft Teams webhook:'
                         + f'\nStatus Code: {response.status_code}\nResponse: {response.text}')


class TwilioNotificationSender(NotificationSender):
    """Provides an API for sending mail notifications."""

    SERVICE: NotificationServiceEnum = NotificationServiceEnum.TWILIO
    """Defines the service name that this sender represents."""

    service: TwilioNotificationService
    """Defines the service configuration to be used for this sender instance."""

    def send(self, recipient: TwilioServiceRecipient):
        """Sends a notification to the given service recipient for the given event."""
        import time
        from loguru import logger
        from twilio.rest import Client
        from app import config
        from app.lib.config.services import ServicesConfig

        try:
            super().send(recipient)
        except NotImplementedError:
            pass

        sender: Optional[ServicesConfig.TwilioConfig.TwilioNumberConfig] = None

        for number in config.services.twilio.numbers:
            if not number.sms:
                continue
            sender = number
            break

        if not isinstance(sender, ServicesConfig.TwilioConfig.TwilioNumberConfig):
            logger.warning(
                f'Unable to send Twilio message to {recipient.label} with no SMS capable numbers configured!')
            return

        message = ''

        if isinstance(message_title := self.event.message_title, str):
            message += f'{message_title}\n\n'

        if isinstance(message_body := self.event.message_body_plain, str):
            message += f'{message_body}'

        logger.debug(f'Sending notification SMS: Config: {self.config.label}, Recipient: {recipient.label}, '
                     + f'Category: {self.event.category}')

        client = Client(config.services.twilio.api.live.account_sid, config.services.twilio.api.live.auth_token)

        messages_sent = []

        messages_sent.append(client.messages.create(
            body=message,
            from_=sender.number,
            to=recipient.number,
        ))

        time.sleep(2)

        for result in messages_sent:
            msg = client.messages(result.sid).fetch()

            log_msg = f'Sent Twilio message: From: {msg.from_}, To: {msg.to} ({recipient.label}), Status: {msg.status}'

            if msg.price is not None:
                log_msg += f', Price: {msg.price} {msg.price_unit}'

            log_msg += f'\nMessage:\n{msg.body}'

            logger.debug(log_msg)


ALL_SENDERS = Union[MailNotificationSender, MsTeamsNotificationSender, TwilioNotificationSender]
ALL_SENDERS_TYPE = type[ALL_SENDERS]


class NotificationManager:
    """Provides an API for handling notification events and sending notifications."""

    SENDERS: dict[NotificationServiceEnum, ALL_SENDERS_TYPE] = {
        NotificationServiceEnum.MAIL: MailNotificationSender,
        NotificationServiceEnum.MSTEAMS: MsTeamsNotificationSender,
        NotificationServiceEnum.TWILIO: TwilioNotificationSender,
    }

    _configs: list[NotificationConfig]

    def __init__(self, configs: Optional[list[NotificationConfig]] = None):
        """Initializes the notification manager."""

        if not isinstance(configs, list):
            from app import notifications
            configs = notifications

        self._configs = configs

    def handle_event(self, event: ALL_EVENTS):
        """Handles one or more notification events and sends appropriate notifications."""

        now = datetime.now(tz=UTC_TZ)

        # Filter the loaded notification configuration objects to only those that are applicable to the given event
        configs = self.get_event_configurations(event=event, timestamp=now)

        # Send notifications for each matching notification configuration
        self.send_notifications(event=event, configs=configs, timestamp=now)

    def get_event_configurations(self, event: ALL_EVENTS, timestamp: Optional[datetime] = None) -> list[
        NotificationConfig]:
        """Provides a list of notification configurations for a particular event."""

        configs = []

        for nc in self._configs:
            if nc.applicable(event=event, timestamp=timestamp):
                configs.append(nc)

        return configs

    def get_service_sender(self, service: NotificationServiceEnum) -> ALL_SENDERS_TYPE:
        """Retrieves the notification sender class associated with the given service identifier."""

        if service not in self.SENDERS:
            raise ValueError(f'Service {service} is not supported!')

        return self.SENDERS[service]

    def send_notifications(self, event: ALL_EVENTS, configs: list[NotificationConfig],
                           timestamp: Optional[datetime] = None):
        """Sends notifications for the given event based on the given configurations."""

        for config in configs:
            if not isinstance(config.services, list) or not config.services:
                continue

            for service in config.services:
                # TODO: Check if service is enabled in global configuration

                if not service.enabled or not service.applicable(timestamp=timestamp):
                    continue

                if not isinstance(service.recipients, list) or not service.recipients:
                    continue

                sender = self.get_service_sender(service=service.name)(event=event, config=config, service=service)

                for recipient in service.recipients:
                    if not recipient.enabled or not recipient.applicable(timestamp=timestamp):
                        continue

                    sender.send(recipient=recipient)
