from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from app.decorators.request import verify_user

UserModel = get_user_model()
view_directory: str = 'account/create'


@login_required
@verify_user
def create(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's1-org-meta.jinja2'))


@login_required
@verify_user
def create_domains(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's2-domains.jinja2'))


@login_required
@verify_user
def create_invite(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's3-invite.jinja2'))


@login_required
@verify_user
def create_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 's4-done.jinja2'))

