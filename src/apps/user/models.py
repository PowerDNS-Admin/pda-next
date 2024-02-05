import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.data.models import Country, Timezone


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15, null=True)
    is_setup = models.BooleanField(default=False)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='user_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
