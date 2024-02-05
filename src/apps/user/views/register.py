from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.urls import reverse_lazy

UserModel = get_user_model()
view_directory: str = 'user/register'


def register(request: HttpRequest):
    import os
    from django.shortcuts import redirect, render
    from apps.user.forms.register import RegistrationForm

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.status = UserModel.STATUS_PENDING_SETUP
            user.save()
            return redirect(reverse_lazy('user:index'))
    else:
        form = RegistrationForm()

    return render(request, os.path.join(view_directory, 'register.jinja2'), {'form': form})
