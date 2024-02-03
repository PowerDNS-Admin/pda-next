from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

UserModel = get_user_model()
view_directory: str = 'account'


@login_required
def index(request: HttpRequest):
    import os
    import uuid
    from django.shortcuts import redirect, render, reverse
    from apps.account.models import Account, AccountUser
    from apps.data.models import Country, Timezone
    from apps.user.models import User

    user: User = User.objects.filter(user=request.user).first()

    link: AccountUser = AccountUser.objects.filter(user=user).first()

    if link is None:
        return redirect(reverse('account:start'))

    account: Account = Account.objects.filter(pk=link.account.id).first()
    exists: bool = account is not None

    if account is None:
        account = Account()

    if request.method == 'POST':
        account.org_name = request.POST.get('org_name')
        account.country = Country.objects.get(pk=request.POST.get('country'))
        account.timezone = Timezone.objects.get(pk=request.POST.get('timezone'))

        if account.uuid is None:
            account.uuid = uuid.uuid4()

        account.is_setup = True
        account.save()

        link = AccountUser(account=account, user=user, role='owner')
        link.save()

        if exists:
            return redirect(reverse('account:index'))

        # Send the user to the second step of account setup (not implemented yet)
        return redirect(reverse('account:index'))

    params: dict = {
        'account': account,
        'countries': Country.objects.all(),
        'timezones': Timezone.objects.all(),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


@login_required
def start(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'start.jinja2'))


@login_required
def create(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s1-org-meta.jinja2'))


@login_required
def create_domains(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s2-domains.jinja2'))


@login_required
def create_invite(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s3-invite.jinja2'))


@login_required
def create_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'create/s4-done.jinja2'))


@login_required
def domains(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'domains/index.jinja2'))


@login_required
def domain_add(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'domains/add.jinja2'))


@login_required
def domain_remove(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'domains/remove.jinja2'))


@login_required
def invite(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'invite/s1-lookup.jinja2'))


@login_required
def invite_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'invite/s2-done.jinja2'))


@login_required
def join(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'join/s1-lookup.jinja2'))


@login_required
def join_verify(request: HttpRequest, token: str = None):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'join/s2-verify.jinja2'))


@login_required
def join_done(request: HttpRequest):
    import os
    from django.shortcuts import render

    return render(request, os.path.join(view_directory, 'join/s3-done.jinja2'))
