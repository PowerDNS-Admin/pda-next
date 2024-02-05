from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from apps.user.models import User


@login_required
def index(request):
    user: User = request.user

    if user is None or user.pk and not user.is_setup:
        return redirect(reverse('user:index'))

    params: dict = {}

    return render(request, 'dashboard/index.jinja2', params)
