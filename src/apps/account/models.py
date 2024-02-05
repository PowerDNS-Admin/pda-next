import uuid
from django.db import models
from apps.user.models import User


class Account(models.Model):
    from apps.data.models import Country, Timezone

    STATUS_DRAFT = 'draft'
    STATUS_PENDING_VERIFICATION = 'pending-verification'
    STATUS_PENDING_APPROVAL = 'pending-approval'
    STATUS_PENDING_SETUP = 'pending-setup'
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_LOCKED = 'locked'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_DRAFT, STATUS_PENDING_VERIFICATION, STATUS_PENDING_APPROVAL, STATUS_PENDING_SETUP, STATUS_ACTIVE,
                STATUS_INACTIVE, STATUS_LOCKED, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    org_name = models.CharField(max_length=30, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default=STATUS_DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountDomain(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PENDING_VERIFICATION = 'pending-verification'
    STATUS_PENDING_APPROVAL = 'pending-approval'
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_LOCKED = 'locked'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_DRAFT, STATUS_PENDING_VERIFICATION, STATUS_PENDING_APPROVAL, STATUS_ACTIVE, STATUS_INACTIVE,
                STATUS_LOCKED, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)
    status = models.CharField(max_length=30, default=STATUS_DRAFT)
    is_stopgap = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountUser(models.Model):
    from apps.user.models import User

    ROLE_OWNER = 'owner'
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLES = [ROLE_OWNER, ROLE_ADMIN, ROLE_USER]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accountuser_user')
    role = models.CharField(max_length=30, default=ROLE_USER)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accountuser_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountInvitation(models.Model):
    from apps.user.models import User

    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELED = 'canceled'
    STATUS_EXPIRED = 'expired'
    STATUS_INVALID = 'invalid'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_DRAFT, STATUS_PENDING, STATUS_ACCEPTED, STATUS_REJECTED, STATUS_CANCELED, STATUS_EXPIRED,
                STATUS_INVALID, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accountinvitation_user')
    email = models.EmailField()
    role = models.CharField(max_length=30, default=AccountUser.ROLE_USER)
    status = models.CharField(max_length=30, default=STATUS_DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='accountinvitation_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
