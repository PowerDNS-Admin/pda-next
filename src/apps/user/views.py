from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.http import HttpRequest
from django.urls import reverse_lazy
from app.decorators.request import verify_user
from apps.user.forms import PasswordResetForm

UserModel = get_user_model()
view_directory: str = 'user'


class PasswordChangeView(BasePasswordChangeView):
    success_url = reverse_lazy('user:password_change_done')
    template_name = 'user/password/change.jinja2'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    success_url = reverse_lazy('user:password_reset_complete')
    template_name = 'user/password/reset_confirm.jinja2'


def notification_test(request: HttpRequest):
    from django.http import JsonResponse
    from app import config
    from apps.notifications.lib import NotificationManager
    from apps.notifications.models import Notification
    from apps.user.models import User

    user: User = request.user

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


def login(request: HttpRequest):
    import os
    from django.contrib.auth import authenticate
    from django.contrib.auth.forms import AuthenticationForm
    from django.shortcuts import redirect, render, reverse
    from loguru import logger

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


@login_required
def index(request: HttpRequest):
    import os
    from django.shortcuts import redirect, render, reverse
    from apps.user.models import User
    from apps.data.models import Country, Timezone

    user: User = User.objects.filter(pk=request.user.pk).first()
    exists: bool = user is not None

    if user is None:
        user = request.user

    if request.method == 'POST':
        user.country = Country.objects.get(pk=request.POST.get('country'))
        user.timezone = Timezone.objects.get(pk=request.POST.get('timezone'))

        user.status = User.STATUS_ACTIVE
        user.save()

        if exists:
            return redirect(reverse('user:index'))

        # Send the user to the second step of user setup (not implemented yet)
        return redirect(reverse('user:index'))

    params: dict = {
        'app_user': user,
        'countries': Country.objects.all(),
        'timezones': Timezone.objects.all(),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


def register(request: HttpRequest):
    import os
    from django.shortcuts import redirect, render
    from apps.user.models import User
    from .forms import RegistrationForm

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.status = User.STATUS_PENDING_SETUP
            user.save()
            return redirect(reverse_lazy('user:index'))
    else:
        form = RegistrationForm()

    return render(request, os.path.join(view_directory, 'register.jinja2'), {'form': form})


@login_required
@verify_user
def change_password(request: HttpRequest):
    import os
    from django.contrib.auth.forms import PasswordChangeForm
    from django.shortcuts import redirect, render

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('user:password_change_done'))
    else:
        form = PasswordChangeForm(request.user)

    return render(request, os.path.join(view_directory, 'password/change.jinja2'), {'form': form})


@login_required
@verify_user
def change_password_done(request: HttpRequest):
    import os
    from django.shortcuts import render
    return render(request, os.path.join(view_directory, 'password/change_done.jinja2'))


def password_reset(request: HttpRequest):
    import os
    from django.shortcuts import redirect, render
    from app import config

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            options = {
                'from_email': config.email.from_email().ref,
                'request': request,
            }
            form.save(**options)
            return redirect(reverse_lazy('user:password_reset_done'))
    else:
        form = PasswordResetForm()

    return render(request, os.path.join(view_directory, 'password/reset.jinja2'), {'form': form})


def password_reset_confirm(request: HttpRequest):
    import os
    from django.contrib.auth.forms import SetPasswordForm
    from django.shortcuts import redirect, render

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('user:password_reset_complete'))
    else:
        form = SetPasswordForm(request.user)

    return render(request, os.path.join(view_directory, 'password/reset_confirm.jinja2'), {'form': form})
