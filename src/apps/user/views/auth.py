from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView,
)

UserModel = get_user_model()
view_directory: str = 'user/auth'


class LogoutView(BaseLogoutView):
    template_name = f'{view_directory}/logout.jinja2'


def login(request: HttpRequest):
    import os
    from django.contrib.auth import authenticate
    from django.shortcuts import redirect, render, reverse
    from loguru import logger
    from apps.user.forms.auth import AuthenticationForm

    if request.user.is_authenticated:
        return redirect(reverse('user:index'))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')

        user: UserModel = UserModel()
        user.username = username
        user.set_password(password)

        if user.check_password(password) and not user.is_active:
            logger.warning(f'User {username} attempted to login but their user is disabled.')
            form.add_error(None, 'Your user is disabled.')

        elif form.is_valid():
            user = authenticate(request, username=username, password=password)
            from django.contrib.auth import login
            login(request, user)
            return redirect(reverse('user:index'))
    else:
        form = AuthenticationForm()

    return render(request, os.path.join(view_directory, 'login.jinja2'), {'form': form})


def notification_test(request: HttpRequest):
    from django.http import JsonResponse
    from app import config
    from apps.notifications.lib import NotificationManager
    from apps.notifications.models import Notification

    user: UserModel = request.user

    params = {
        'label': 'Test Notification',
        'notification_format': Notification.FORMAT_ALL,
        'created_by': user,
        'urgent': True,
    }

    notification = NotificationManager.create(**params)
    notification.save()

    email_params = {
        'from_email': config.email.from_email().ref,
        'subject': 'Test Notification',
        'text_body': 'PowerDNS Admin\n\nThis is a test notification.',
        'html_body': '<h2>PowerDNS Admin</h2><p>This is a test notification.</p>',
    }

    email = NotificationManager.create_email(notification, **email_params)
    email.save()

    call_params = {
        'message': 'This is a test notification.',
    }

    call = NotificationManager.create_call(notification, **call_params)
    call.save()

    text_params = {
        'sms_body': 'This is a test notification.',
    }

    text = NotificationManager.create_text(notification, **text_params)
    text.save()

    recipient = NotificationManager.create_email_recipient(notification, user.email)
    recipient.phone = user.phone
    recipient.user = user
    recipient.save()

    # Schedule the notification for sending ASAP if marked urgent
    if notification.urgent:
        from apps.notifications.tasks import send_notification
        send_notification.delay(notification.pk)

    # Otherwise, mark the notification as pending and let the scheduler handle it
    else:
        notification.status = Notification.STATUS_PENDING
        notification.save()

    return JsonResponse({'status': 'success'})
