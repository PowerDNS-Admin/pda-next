from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import auth, password, profile, register

app_name = 'user'
urlpatterns = [
    # Profile Actions
    path('', profile.index, name='index'),
    path('/', RedirectView.as_view(url=f'/{app_name}', permanent=False), name='index_redirect'),

    # Authentication Actions
    path('/login', views.auth.login, name='login'),
    path('/logout', auth.LogoutView.as_view(), name='logout'),

    # Registration Actions
    path('/register', register.register, name='register'),

    # Password Change Actions
    path('/change-password', password.PasswordChangeView.as_view(), name='password.change'),
    path('/change-password/done', password.change_password_done, name='password.change_done'),

    # Password Reset Actions
    path('/reset-password', password.password_reset, name='password.reset'),
    path('/reset-password/done', password.PasswordResetDoneView.as_view(), name='password.reset_done'),
    path('/reset-password/confirm/<str:uidb64>/<str:token>', password.PasswordResetConfirmView.as_view(),
         name='password.reset_confirm'),
    path('/reset-password/complete', password.PasswordResetCompleteView.as_view(), name='password.reset_complete'),
]
