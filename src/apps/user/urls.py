from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('/', RedirectView.as_view(url='/user', permanent=False), name='index_redirect'),
    path('/login', views.login, name='login'),
    path('/logout', LogoutView.as_view(template_name='user/logout.jinja2'), name='logout'),
    path('/change-password', views.PasswordChangeView.as_view(), name='password_change'),
    path('/change-password/done', views.change_password_done, name='password_change_done'),
    path('/reset-password', views.password_reset, name='password_reset'),
    path('/reset-password/done', PasswordResetDoneView.as_view(template_name='user/password_reset_done.jinja2'),
         name='password_reset_done'),
    path('/reset-password/confirm/<str:uidb64>/<str:token>', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('/reset-password/complete',
         PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.jinja2'),
         name='password_reset_complete'),
    path('/register', views.register, name='register'),
]
