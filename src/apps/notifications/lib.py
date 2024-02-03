from apps.notifications.models import Notification, NotificationEmail, NotificationCall, NotificationText, \
    NotificationRecipient
from apps.user.models import User


class NotificationManager:
    """ The NotificationManager class provides an interface for creating and managing notifications. """

    @staticmethod
    def create(label: str, notification_format: int, created_by: User, urgent: bool = False) -> Notification:
        return Notification(label=label, format=notification_format, created_by=created_by,
                            urgent=urgent)

    @staticmethod
    def create_email(notification: Notification, from_email: str, subject: str,
                     text_body: str = None, html_body: str = None) -> NotificationEmail:
        return NotificationEmail(notification=notification, from_email=from_email, subject=subject,
                                 text_body=text_body, html_body=html_body)

    @staticmethod
    def create_call(notification: Notification, message: str) -> NotificationCall:
        return NotificationCall(notification=notification, created_by=notification.created_by, message=message)

    @staticmethod
    def create_text(notification: Notification, sms_body: str = None, mms_body: str = None) -> NotificationText:
        return NotificationText(notification=notification, created_by=notification.created_by, sms_body=sms_body, mms_body=mms_body)

    @staticmethod
    def create_email_recipient(notification: Notification, email: str) -> NotificationRecipient:
        return NotificationRecipient(notification=notification, created_by=notification.created_by, email=email)

    @staticmethod
    def create_phone_recipient(notification: Notification, phone: str) -> NotificationRecipient:
        return NotificationRecipient(notification=notification, created_by=notification.created_by, phone=phone)

    @staticmethod
    def create_user_recipient(notification: Notification, user: User) -> NotificationRecipient:
        return NotificationRecipient(notification=notification, created_by=notification.created_by, user=user)
