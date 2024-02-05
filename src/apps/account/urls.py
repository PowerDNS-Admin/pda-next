from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import create, domains, invite, join

app_name = 'account'
urlpatterns = [
    path('', views.index, name='index'),
    path('/', RedirectView.as_view(url=f'/{app_name}', permanent=False), name='index_redirect'),
    path('/start', views.start, name='start'),
    path('/create', create.create, name='create'),
    path('/create/domains', create.create_domains, name='create.domains'),
    path('/create/invite', create.create_invite, name='create.invite'),
    path('/create/done', create.create_done, name='create.done'),
    path('/domains', domains.domains, name='domains'),
    path('/domains/add', domains.domain_add, name='domain.add'),
    path('/domains/remove', domains.domain_remove, name='domain.remove'),
    path('/invite', invite.invite, name='invite'),
    path('/invite/done', invite.invite_done, name='invite.done'),
    path('/join', join.join, name='join'),
    path('/join/verify/<str:token>', join.join_verify, name='join.verify_token'),
    path('/join/verify', join.join_verify, name='join.verify'),
    path('/join/done', join.join_done, name='join.done'),
]
