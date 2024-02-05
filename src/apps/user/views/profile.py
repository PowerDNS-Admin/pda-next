from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

UserModel = get_user_model()
view_directory: str = 'user/profile'


@login_required
def index(request: HttpRequest):
    import os
    from django.shortcuts import redirect, render, reverse
    from apps.data.models import Country, Timezone

    user: UserModel = UserModel.objects.filter(pk=request.user.pk).first()
    exists: bool = user is not None

    if user is None:
        user = request.user

    if request.method == 'POST':
        user.country = Country.objects.get(pk=request.POST.get('country'))
        user.timezone = Timezone.objects.get(pk=request.POST.get('timezone'))

        user.status = UserModel.STATUS_ACTIVE
        user.save()

        if exists:
            return redirect(reverse('user:index'))

        # Send the user to the second step of user setup (not implemented yet)
        return redirect(reverse('user:index'))

    params: dict = {
        'app_user': user,
        'countries': Country.objects.all(),
        'timezones': Timezone.objects.all(),
    }

    return render(request, os.path.join(view_directory, 'index.jinja2'), params)
