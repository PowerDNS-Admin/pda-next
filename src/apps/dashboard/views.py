from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from apps.account.models import Account


@login_required
def index(request):
    account = Account.objects.filter(user=request.user).first()

    if account is None or account.pk and not account.is_setup:
        return redirect(reverse('account:index'))

    params: dict = {}

    return render(request, 'dashboard/index.jinja2', params)
