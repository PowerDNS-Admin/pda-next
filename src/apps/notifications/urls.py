from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'notifications'
urlpatterns = [
    path('', views.index, name='index'),
    path('/', RedirectView.as_view(url=f'/{app_name}', permanent=False), name='index_redirect'),
]
