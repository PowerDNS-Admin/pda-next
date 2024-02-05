import uuid
from django.db import models
from apps.user.models import User


class Account(models.Model):
    from apps.data.models import Country, Timezone

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    org_name = models.CharField(max_length=30, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE)
    is_setup = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountDomain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)
    is_pending = models.BooleanField(default=True)
    is_stopgap = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountUser(models.Model):
    from apps.user.models import User

    ROLE_OWNER = 'owner'
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accountuser_user')
    role = models.CharField(max_length=30, default=ROLE_USER)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accountuser_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountInvitation(models.Model):
    from apps.user.models import User

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accountinvitation_user')
    email = models.EmailField()
    role = models.CharField(max_length=30, default=AccountUser.ROLE_USER)
    is_admin = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_invalid = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='accountinvitation_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
