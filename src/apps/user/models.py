from django.db import models
from django.contrib.auth.models import User as BaseUser
from apps.data.models import Country, Timezone


class User(models.Model):
    uuid = models.UUIDField(default=None, null=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE)
    is_setup = models.BooleanField(default=False)
