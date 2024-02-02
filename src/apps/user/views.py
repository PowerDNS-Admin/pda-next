from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.http import HttpRequest
from django.urls import reverse_lazy

UserModel = get_user_model()
view_directory: str = 'user'


class PasswordChangeView(BasePasswordChangeView):
    success_url = reverse_lazy('user:password_change_done')
    template_name = 'user/password_change.jinja2'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    success_url = reverse_lazy('user:password_reset_complete')
    template_name = 'user/password_reset_confirm.jinja2'


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
    import uuid
    from django.shortcuts import redirect, render, reverse
    from apps.user.models import User
    from apps.data.models import Country, Timezone

    user: User = User.objects.filter(user=request.user).first()
    exists: bool = user is not None

    if user is None:
        user = User(user=request.user)

    if request.method == 'POST':
        user.country = Country.objects.get(pk=request.POST.get('country'))
        user.timezone = Timezone.objects.get(pk=request.POST.get('timezone'))

        if user.uuid is None:
            user.uuid = uuid.uuid4()

        user.is_setup = True
        user.save()

        if exists:
            return redirect(reverse('user:index'))

        # Send the user to the second step of user setup (not implemented yet)
        return redirect(reverse('user:index'))

    params: dict = {
        'user': user,
        'countries': Country.objects.all(),
        'timezones': Timezone.objects.all(),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


def register(request: HttpRequest):
    import os
    from django.shortcuts import redirect, render
    from .forms import RegistrationForm

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            return redirect(reverse_lazy('user:index'))
    else:
        form = RegistrationForm()

    return render(request, os.path.join(view_directory, 'register.jinja2'), {'form': form})


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

    return render(request, os.path.join(view_directory, 'password_change.jinja2'), {'form': form})


def change_password_done(request: HttpRequest):
    import os
    from django.shortcuts import render
    return render(request, os.path.join(view_directory, 'password_change_done.jinja2'))


def password_reset(request: HttpRequest):
    import os
    from django.contrib.auth.forms import PasswordResetForm
    from django.shortcuts import redirect, render
    from app import config

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            options = {
                'subject_template_name': 'user/password_reset_subject.jinja2',
                'email_template_name': 'user/password_reset_email_text.jinja2',
                'html_email_template_name': 'user/password_reset_email_html.jinja2',
                'use_https': config.web.protocol().ref == 'https',
                'from_email': config.email.from_email().ref,
                'request': request,
            }
            form.save(**options)
            return redirect(reverse_lazy('user:password_reset_done'))
    else:
        form = PasswordResetForm()

    return render(request, os.path.join(view_directory, 'password_reset.jinja2'), {'form': form})


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

    return render(request, os.path.join(view_directory, 'password_reset_confirm.jinja2'), {'form': form})
