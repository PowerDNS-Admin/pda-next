import os
import uuid
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import redirect, render, reverse
from app import config
from apps.account.models import Account
from apps.data.models import Country, Timezone

UserModel = get_user_model()

view_directory: str = 'account'


def login(request: HttpRequest):
    from loguru import logger

    if request.user.is_authenticated:
        return redirect(reverse('account:index'))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')

        logger.warning(username)
        logger.warning(password)

        user: UserModel = UserModel()
        user.username = username
        user.set_password(password)

        logger.warning(user.check_password(password))

        if user.check_password(password) and not user.is_active:
            logger.warning(f'User {username} attempted to login but their account is disabled.')
            form.add_error(None, 'Your account is disabled.')

        elif form.is_valid():
            user = authenticate(request, username=username, password=password)

            logger.warning(user)

            from django.contrib.auth import login
            login(request, user)
            return redirect(reverse('account:index'))
    else:
        form = AuthenticationForm()

    params: dict = {
        'form': form,
    }

    return render(request, os.path.join(view_directory, 'login.jinja2'), params)


@login_required
def index(request: HttpRequest):
    account: Account = Account.objects.filter(user=request.user).first()
    exists: bool = account is not None

    if account is None:
        account = Account(user=request.user)

    if request.method == 'POST':
        account.org_name = request.POST.get('org_name')
        account.country = Country.objects.get(pk=request.POST.get('country'))
        account.timezone = Timezone.objects.get(pk=request.POST.get('timezone'))

        if account.uuid is None:
            account.uuid = uuid.uuid4()

        account.save()

        if exists:
            return redirect(reverse('account:index'))

        # Send the user to the second step of account setup
        return redirect(reverse('account:prompts'))

    params: dict = {
        'account': account,
        'countries': Country.objects.all(),
        'timezones': Timezone.objects.all(),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)


def register(request: HttpRequest):
    from .forms import RegistrationForm

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/account')
    else:
        form = RegistrationForm()

    params: dict = {'form': form}

    return render(request, os.path.join(view_directory, 'register.jinja2'), params)
