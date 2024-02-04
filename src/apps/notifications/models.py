import uuid
from django.db import models
from apps.user.models import User


class Notification(models.Model):
    FORMAT_ALL = 0
    FORMAT_EMAIL = 1
    FORMAT_CALL = 2
    FORMAT_TEXT = 3

    STATUS_DRAFT = 0
    STATUS_PENDING = 1
    STATUS_SENDING = 2
    STATUS_SENT = 3
    STATUS_FAILED = 4

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    label = models.CharField(max_length=255, null=True)
    format = models.IntegerField(default=FORMAT_EMAIL)
    urgent = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    send_at = models.DateTimeField(null=True)
    sent_at = models.DateTimeField(null=True)
    status = models.IntegerField(default=STATUS_DRAFT)

    @property
    def is_all(self):
        return self.format == self.FORMAT_ALL

    @property
    def is_email(self):
        return self.format == self.FORMAT_ALL or self.format == self.FORMAT_EMAIL

    @property
    def is_call(self):
        return self.format == self.FORMAT_ALL or self.format == self.FORMAT_CALL

    @property
    def is_text(self):
        return self.format == self.FORMAT_ALL or self.format == self.FORMAT_TEXT

    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING

    @property
    def is_sending(self):
        return self.status == self.STATUS_SENDING

    @property
    def is_sent(self):
        return self.status == self.STATUS_SENT

    @property
    def is_failed(self):
        return self.status == self.STATUS_FAILED

    @property
    def send_at_local(self):
        import time
        from datetime import timedelta, timezone

        if self.send_at is None:
            return None

        offset: timedelta = timedelta(seconds=self.user.timezone.offset)

        if time.daylight:
            offset += timedelta(seconds=3600)

        local_tz = timezone(offset, self.user.timezone.name)
        return self.send_at.astimezone(local_tz)

    @property
    def send_at_field(self):
        if self.send_at_local is None:
            return None
        return self.send_at_local.strftime('%m/%d/%Y %I:%M %p')

    @property
    def send_at_date(self):
        if self.send_at_local is None:
            return None
        return self.send_at_local.strftime('%m/%d/%Y')

    @property
    def send_at_time(self):
        if self.send_at_local is None:
            return None
        return self.send_at_local.strftime('%I:%M %p')

    @property
    def send_at_text(self):
        if self.send_at_local is None:
            return 'Immediately'
        return self.send_at_local.strftime('%m/%d/%Y @ %I:%M %p')

    @property
    def send_at_html(self):
        if self.send_at_local is None:
            return 'Send<br/>Immediately'
        return f'{self.send_at_date}<br/>{self.send_at_time}'

    @property
    def format_text(self):
        if self.is_all:
            return 'All'
        if self.is_email:
            return 'Email'
        if self.is_call:
            return 'Call'
        if self.is_text:
            return 'Text'
        return 'Unknown'

    @property
    def format_icon(self):
        if self.is_all:
            return 'fa fa-mobile-screen-button'
        if self.is_email:
            return 'fa fa-envelope'
        if self.is_call:
            return 'fa fa-phone'
        if self.is_text:
            return 'fa fa-message'
        return 'fa fa-question'

    @property
    def status_text(self):
        if self.is_pending:
            return 'Pending'
        elif self.is_sending:
            return 'Sending'
        elif self.is_sent:
            return 'Sent'
        elif self.is_failed:
            return 'Failed'
        else:
            return 'Unknown'

    @property
    def status_icon(self):
        if self.is_pending:
            return 'fa fa-clock'
        elif self.is_sending:
            return 'fa fa-spinner'
        elif self.is_sent:
            return 'fa fa-check'
        elif self.is_failed:
            return 'fa fa-xmark'
        else:
            return 'fa fa-question'


class NotificationEmail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    from_email = models.EmailField(null=True)
    subject = models.CharField(max_length=255, null=True)
    text_body = models.TextField(null=True)
    html_body = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationText(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    sms_body = models.TextField(null=True)
    mms_body = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationRecipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notificationrecipient_user')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='notificationrecipient_crated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationLog(models.Model):
    STATUS_PENDING = 0
    STATUS_SENDING = 1
    STATUS_SENT = 2
    STATUS_FAILED = 3

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    recipient = models.ForeignKey(NotificationRecipient, on_delete=models.CASCADE)
    format = models.IntegerField(default=Notification.FORMAT_ALL)
    data = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True)
    status = models.IntegerField(default=STATUS_PENDING)
