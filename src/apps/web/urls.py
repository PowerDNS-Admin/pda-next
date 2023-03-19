from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "web"
urlpatterns = [
    path("", views.home, name="home"),
    path("terms/", TemplateView.as_view(template_name="web/terms.html"), name="terms"),
    # these views are just for testing error pages
    # actual error handling is handled by Django: https://docs.djangoproject.com/en/4.1/ref/views/#error-views
    path("400/", TemplateView.as_view(template_name="400.html"), name="400"),
    path("403/", TemplateView.as_view(template_name="403.html"), name="403"),
    path("404/", TemplateView.as_view(template_name="404.html"), name="404"),
    path("500/", TemplateView.as_view(template_name="500.html"), name="500"),
    path("send_test_email/", views.send_test_email),
    path("simulate_error/", views.simulate_error),
]
