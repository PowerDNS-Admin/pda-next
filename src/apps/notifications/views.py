from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

view_directory: str = 'notifications'


@login_required
def index(request: HttpRequest):
    import os
    from django.shortcuts import render
    return render(request, os.path.join(view_directory, 'index.jinja2'))
