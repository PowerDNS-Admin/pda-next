from django.db import models
from django.contrib.auth.models import User
from apps.data.models import Country, Timezone


class Account(models.Model):
    uuid = models.UUIDField(default=None, null=True)
    org_name = models.CharField(max_length=30, null=True)
    is_setup = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE)
