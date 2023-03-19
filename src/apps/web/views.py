from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def home(request):
    if request.user.is_authenticated:
        return render(
            request,
            'web/app_home.html',
            context={
                'active_tab': 'dashboard',
                'page_title': _('Dashboard'),
            },
        )
    else:
        return render(request, 'web/landing_page.html')


def send_test_email(request):
    from django.core.mail import send_mail
    from config import settings

    send_mail(
        subject='This is a test email',
        message='This is a test email.',
        from_email=settings.site_from_email,
        recipient_list=[settings.admin_email],
    )
    messages.success(request, 'Test email sent.')
    return HttpResponseRedirect(reverse('home'))


def simulate_error(request):
    raise Exception('This is a simulated error.')
