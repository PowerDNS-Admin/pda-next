from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from app.decorators.request import verify_user


@login_required
@verify_user
def index(request: HttpRequest):
    params: dict = {}
    return render(request, 'dashboard/index.jinja2', params)
