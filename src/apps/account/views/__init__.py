from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from app.decorators.request import verify_user, has_account

UserModel = get_user_model()
view_directory: str = 'account'


@login_required
@verify_user
@has_account
def index(request: HttpRequest):
    import os
    from django.shortcuts import render
    from apps.data.models import Country, Timezone

    params: dict = {
        'countries': Country.objects.all(),
        'timezones': Timezone.objects.all(),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


@login_required
@verify_user
def start(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'start.jinja2'))
