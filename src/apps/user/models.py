import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.data.models import Country, Timezone


class User(AbstractUser):
    """ This model is used to override the default Django User model """

    STATUS_DRAFT = 'draft'
    STATUS_PENDING_VERIFICATION = 'pending-verification'
    STATUS_PENDING_APPROVAL = 'pending-approval'
    STATUS_PENDING_SETUP = 'pending-setup'
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_DRAFT, STATUS_PENDING_VERIFICATION, STATUS_PENDING_APPROVAL, STATUS_PENDING_SETUP, STATUS_ACTIVE,
                STATUS_INACTIVE, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=30, default=STATUS_DRAFT)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='user_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
