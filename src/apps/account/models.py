from django.db import models


class Account(models.Model):
    from apps.data.models import Country, Timezone

    uuid = models.UUIDField(default=None, null=True)
    org_name = models.CharField(max_length=30, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE)
    is_setup = models.BooleanField(default=False)


class AccountInvitation(models.Model):
    from apps.user.models import User

    uuid = models.UUIDField(default=None, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    role = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_invalid = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountUser(models.Model):
    from apps.user.models import User

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)
