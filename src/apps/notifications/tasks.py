import datetime

from pda.celery import app as celery


@celery.task(name='pda.notifications.send_notifications')
def send_notifications() -> bool:
    from datetime import datetime, timedelta, timezone
    from loguru import logger
    from apps.notifications.models import Notification

    now: datetime = datetime.now(timezone.utc)
    window: timedelta = timedelta(seconds=15)
    notifications = Notification.objects.filter(status=Notification.STATUS_PENDING)

    for notification in notifications:
        try:
            if notification.send_at is not None and notification.send_at.astimezone(timezone.utc) > now - window:
                continue
            send_notification.delay(notification.pk)
        except Exception as e:
            logger.error(f'Error sending notification: {e}')
            notification.status = Notification.STATUS_FAILED
            notification.save()

    return True


@celery.task(name='pda.notifications.send_notification')
def send_notification(notification_id: str) -> bool:
    from loguru import logger
    from app.model.tasks import TaskGroup
    from apps.notifications.models import Notification, NotificationEmail, NotificationCall, NotificationText

    notification = Notification.objects.get(pk=notification_id)

    try:
        notification.status = Notification.STATUS_SENDING
        notification.save()

        tg: TaskGroup = TaskGroup(name=f'notifications.send_notification({notification_id})')

        if notification.format == Notification.FORMAT_ALL or notification.format == Notification.FORMAT_EMAIL:
            emails = NotificationEmail.objects.filter(notification=notification)

            for email in emails:
                task_name = f'notifications.send_email({notification_id}, {email.pk})'
                task = send_email.delay(email.pk)
                tg.create_task(task_name, task.id)

        if notification.format == Notification.FORMAT_ALL or notification.format == Notification.FORMAT_CALL:
            calls = NotificationCall.objects.filter(notification=notification)

            for call in calls:
                task_name = f'notifications.send_call({notification_id}, {call.pk})'
                task = send_call.delay(call.pk)
                tg.create_task(task_name, task.id)

        if notification.format == Notification.FORMAT_ALL or notification.format == Notification.FORMAT_TEXT:
            texts = NotificationText.objects.filter(notification=notification)

            for text in texts:
                task_name = f'notifications.send_text({notification_id}, {text.pk})'
                task = send_text.delay(text.pk)
                tg.create_task(task_name, task.id)

        # Monitor the status of the notification sub-tasks
        monitor_notification.apply_async(args=[notification_id, tg.to_dict()], countdown=10)

    except Exception as e:
        logger.error(f'Error sending notification: {e}')
        notification.status = Notification.STATUS_FAILED
        notification.save()
        return False

    return True


@celery.task(name='pda.notifications.send_email')
def send_email(email_id: str) -> bool:
    from datetime import datetime, timezone
    from django.core.mail import EmailMultiAlternatives
    from app import config
    from apps.notifications.models import Notification, NotificationEmail, NotificationRecipient, NotificationLog

    email = NotificationEmail.objects.get(pk=email_id)
    recipients = NotificationRecipient.objects.filter(notification=email.notification)

    for recipient in recipients:

        log_args = {
            'notification': email.notification,
            'recipient': recipient,
            'format': Notification.FORMAT_EMAIL,
            'status': NotificationLog.STATUS_SENT,
        }

        # Create the email message to be sent
        email_args = [email.subject, email.text_body, config.email.from_email().ref, [recipient.email]]
        message = EmailMultiAlternatives(*email_args)

        # Provide an HTML formatted version if available
        if email.html_body:
            message.attach_alternative(email.html_body, 'text/html')

        try:
            message.send()
        except Exception as e:
            # Log the error
            log_args['status'] = NotificationLog.STATUS_FAILED
            log_args['data'] = str(e)
            log = NotificationLog(**log_args)
            log.save()
            continue

        # Log the success
        log_args['sent_at'] = datetime.now(timezone.utc)
        log = NotificationLog(**log_args)
        log.save()

    return True


@celery.task(name='pda.notifications.send_call')
def send_call(call_id: str) -> bool:
    from datetime import datetime, timezone
    from apps.twilio.tasks import send_call
    from apps.notifications.models import Notification, NotificationCall, NotificationRecipient, NotificationLog

    call = NotificationCall.objects.get(pk=call_id)
    recipients = NotificationRecipient.objects.filter(notification=call.notification)

    success = True

    for recipient in recipients:

        log_args = {
            'notification': call.notification,
            'recipient': recipient,
            'format': Notification.FORMAT_CALL,
            'status': NotificationLog.STATUS_SENT,
        }

        try:
            success, result = send_call(recipient.phone, call.message)

            if not success:
                # Log the error
                log_args['status'] = NotificationLog.STATUS_FAILED
                log_args['data'] = str(result)
                log = NotificationLog(**log_args)
                log.save()
                success = False
                continue

        except Exception as e:
            # Log the error
            log_args['status'] = NotificationLog.STATUS_FAILED
            log_args['data'] = str(e)
            log = NotificationLog(**log_args)
            log.save()
            success = False
            continue

        # Log the success
        log_args['sent_at'] = datetime.now(timezone.utc)
        log = NotificationLog(**log_args)
        log.save()

    return success


@celery.task(name='pda.notifications.send_text')
def send_text(text_id: str) -> bool:
    from datetime import datetime, timezone
    from apps.twilio.tasks import send_text
    from apps.notifications.models import Notification, NotificationText, NotificationRecipient, NotificationLog

    text = NotificationText.objects.get(pk=text_id)
    recipients = NotificationRecipient.objects.filter(notification=text.notification)

    success = True

    for recipient in recipients:

        log_args = {
            'notification': text.notification,
            'recipient': recipient,
            'format': Notification.FORMAT_TEXT,
            'status': NotificationLog.STATUS_SENT,
        }

        try:
            success, result = send_text(recipient.phone, text.sms_body)

            if not success:
                # Log the error
                log_args['status'] = NotificationLog.STATUS_FAILED
                log_args['data'] = str(result)
                log = NotificationLog(**log_args)
                log.save()
                success = False
                continue

        except Exception as e:
            # Log the error
            log_args['status'] = NotificationLog.STATUS_FAILED
            log_args['data'] = str(e)
            log = NotificationLog(**log_args)
            log.save()
            success = False
            continue

        # Log the success
        log_args['sent_at'] = datetime.now(timezone.utc)
        log = NotificationLog(**log_args)
        log.save()

    return success


@celery.task(name='pda.notifications.monitor_notification')
def monitor_notification(notification_id: str, task_group_data: dict) -> bool:
    from celery.result import AsyncResult
    from loguru import logger
    from app.model.tasks import TaskGroup
    from apps.notifications.models import Notification

    notification = Notification.objects.get(pk=notification_id)
    tg: TaskGroup = TaskGroup(**task_group_data)

    logger.debug(f'Monitoring Notification; {tg}')

    for task in tg.tasks:
        result: AsyncResult = AsyncResult(task.id)
        if result.status in ['SUCCESS', 'FAILURE']:
            task.result = result.result

    tg.complete = all(task.result is not None for task in tg.tasks)
    tg.success = all(task.result for task in tg.tasks)

    if not tg.complete:
        logger.debug(f'Notification sending not finished, rescheduling; {tg}')
        monitor_notification.apply_async(args=[notification_id, tg.to_dict()], countdown=10)
        notification.save()
        return True

    if tg.success:
        log_method = logger.success
    else:
        log_method = logger.error

    log_method(f'Notification sending complete; {tg}')

    # Update the notification model with the status
    notification.status = Notification.STATUS_SENT
    notification.save()

    return True
