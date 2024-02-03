from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.index, name='index'),
    path('/', RedirectView.as_view(url=f'/{app_name}', permanent=False), name='index_redirect'),
    path('/start', views.start, name='start'),
    path('/create', views.create, name='create'),
    path('/create/domains', views.create_domains, name='create_domains'),
    path('/create/invite', views.create_invite, name='create_invite'),
    path('/create/done', views.create_done, name='create_done'),
    path('/domains', views.domains, name='domains'),
    path('/domains/add', views.domain_add, name='domain_add'),
    path('/domains/remove', views.domain_remove, name='domain_remove'),
    path('/invite', views.invite, name='invite'),
    path('/invite/done', views.invite_done, name='invite_done'),
    path('/join', views.join, name='join'),
    path('/join/verify/<str:token>', views.join_verify, name='join_verify_token'),
    path('/join/verify', views.join_verify, name='join_verify'),
    path('/join/done', views.join_done, name='join_done'),
]
