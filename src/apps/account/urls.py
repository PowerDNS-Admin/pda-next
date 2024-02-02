from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.index, name='index'),
    path('/', RedirectView.as_view(url='/account', permanent=False), name='index_redirect'),
    path('/start', views.start, name='start'),
    path('/create', views.create, name='create'),
    path('/join', views.join, name='join'),
]
