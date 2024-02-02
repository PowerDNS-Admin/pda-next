from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView, PasswordChangeView,
                                       PasswordChangeDoneView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.index, name='index'),
    path('/', RedirectView.as_view(url='/account', permanent=False), name='index_redirect'),
    path('/login', LoginView.as_view(template_name='account/login.jinja2'), name='login'),
    path('/logout', LogoutView.as_view(template_name='account/logout.jinja2'), name='logout'),
    path('/password-change', PasswordChangeView.as_view(template_name='account/password_change.jinja2'),
         name='password_change'),
    path('/password-change/done', PasswordChangeDoneView.as_view(template_name='account/password_change_done.jinja2'),
         name='password_change_done'),
    path('/password-reset', PasswordResetView.as_view(template_name='account/password_reset.jinja2'),
         name='password_reset'),
    path('/password-reset/complete',
         PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.jinja2'),
         name='password_reset_complete'),
    path('/password-reset/confirm/<str:uidb64>/<str:token>',
         PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.jinja2'),
         name='password_reset_confirm'),
    path('/password-reset/done', PasswordResetDoneView.as_view(template_name='account/password_reset_done.jinja2'),
         name='password_reset_done'),
    path('/register', views.register, name='register'),
]
