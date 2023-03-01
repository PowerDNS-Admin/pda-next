from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

from .models import UserAPIKey


@admin.register(UserAPIKey)
class UserAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = [*APIKeyModelAdmin.list_display, "user"]
