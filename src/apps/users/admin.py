from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display

    fieldsets = UserAdmin.fieldsets + (("Custom Fields", {"fields": ("avatar", "language")}),)
