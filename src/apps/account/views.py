from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from app.decorators.request import verify_user, verify_account

UserModel = get_user_model()
view_directory: str = 'account'


@login_required
@verify_user
@verify_account
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


@login_required
@verify_user
def create(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s1-org-meta.jinja2'))


@login_required
@verify_user
def create_domains(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s2-domains.jinja2'))


@login_required
@verify_user
def create_invite(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s3-invite.jinja2'))


@login_required
@verify_user
def create_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s4-done.jinja2'))


@login_required
@verify_user
@verify_account
def domains(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'domains/index.jinja2'))


@login_required
@verify_user
@verify_account
def domain_add(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'domains/add.jinja2'))


@login_required
@verify_user
@verify_account
def domain_remove(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'domains/remove.jinja2'))


@login_required
@verify_user
@verify_account
def invite(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'invite/s1-lookup.jinja2'))


@login_required
@verify_user
@verify_account
def invite_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'invite/s2-done.jinja2'))


@login_required
@verify_user
def join(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'join/s1-lookup.jinja2'))


@login_required
@verify_user
def join_verify(request: HttpRequest, token: str = None):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'join/s2-verify.jinja2'))


@login_required
@verify_user
def join_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'join/s3-done.jinja2'))
