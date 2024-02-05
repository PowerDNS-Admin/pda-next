from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)
from django.http import HttpRequest
from django.urls import reverse_lazy
from app.decorators.request import verify_user
from apps.user.forms import PasswordResetForm

UserModel = get_user_model()
view_directory: str = 'user/password'


class PasswordChangeView(BasePasswordChangeView):
    success_url = reverse_lazy('user:password.change_done')
    template_name = f'{view_directory}/change.jinja2'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    success_url = reverse_lazy('user:password.reset_complete')
    template_name = f'{view_directory}/reset_confirm.jinja2'


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = f'{view_directory}/reset_done.jinja2'


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name = f'{view_directory}/reset_complete.jinja2'


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
            return redirect(reverse_lazy('user:password.change_done'))
    else:
        form = PasswordChangeForm(request.user)

    return render(request, os.path.join(view_directory, 'change.jinja2'), {'form': form})


@login_required
@verify_user
def change_password_done(request: HttpRequest):
    import os
    from django.shortcuts import render
    return render(request, os.path.join(view_directory, 'change_done.jinja2'))


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
            return redirect(reverse_lazy('user:password.reset_done'))
    else:
        form = PasswordResetForm()

    return render(request, os.path.join(view_directory, 'reset.jinja2'), {'form': form})


def password_reset_confirm(request: HttpRequest):
    import os
    from django.contrib.auth.forms import SetPasswordForm
    from django.shortcuts import redirect, render

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('user:password.reset_complete'))
    else:
        form = SetPasswordForm(request.user)

    return render(request, os.path.join(view_directory, 'reset_confirm.jinja2'), {'form': form})
