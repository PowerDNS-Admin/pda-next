from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from app.decorators.request import verify_user, has_account

UserModel = get_user_model()
view_directory: str = 'account/invite'


@login_required
@verify_user
@has_account
def invite(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's1-lookup.jinja2'))


@login_required
@verify_user
@has_account
def invite_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's2-done.jinja2'))
