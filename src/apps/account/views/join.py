from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from app.decorators.request import verify_user

UserModel = get_user_model()
view_directory: str = 'account/join'


@login_required
@verify_user
def join(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's1-lookup.jinja2'))


@login_required
@verify_user
def join_verify(request: HttpRequest, token: str = None):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's2-verify.jinja2'))


@login_required
@verify_user
def join_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's3-done.jinja2'))
