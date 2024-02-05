from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from app.decorators.request import verify_user, has_account

UserModel = get_user_model()
view_directory: str = 'account/domains'


@login_required
@verify_user
@has_account
def domains(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'index.jinja2'))


@login_required
@verify_user
@has_account
def domain_add(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'add.jinja2'))


@login_required
@verify_user
@has_account
def domain_remove(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'remove.jinja2'))
