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
    STATUS_LOCKED = 'locked'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_DRAFT, STATUS_PENDING_VERIFICATION, STATUS_PENDING_APPROVAL, STATUS_PENDING_SETUP, STATUS_ACTIVE,
                STATUS_INACTIVE, STATUS_LOCKED, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=30, default=STATUS_DRAFT)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='user_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tokens = models.ManyToManyField('UserToken', related_name='user_tokens')
    emails = models.ManyToManyField('UserEmail', related_name='user_emails')
    phones = models.ManyToManyField('UserPhone', related_name='user_phones')
    addresses = models.ManyToManyField('UserAddress', related_name='user_addresses')


class UserToken(models.Model):
    """ This model is used to store user tokens used for security verifications. """
    STATUS_ACTIVE = 'active'
    STATUS_USED = 'used'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'
    STATUSES = [STATUS_ACTIVE, STATUS_USED, STATUS_CANCELLED, STATUS_EXPIRED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default=STATUS_ACTIVE)
    token = models.CharField(max_length=100)
    is_single_use = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True)


class UserEmail(models.Model):
    """ This model is used to store user email addresses. """
    ROLE_PRIMARY = 'primary'
    ROLE_RECOVERY = 'recovery'
    ROLE_PERSONAL = 'personal'
    ROLE_WORK = 'work'
    ROLE_OTHER = 'other'
    ROLE_NOTIFICATIONS = 'notifications'
    ROLES = [ROLE_PRIMARY, ROLE_RECOVERY, ROLE_PERSONAL, ROLE_WORK, ROLE_OTHER, ROLE_NOTIFICATIONS]

    STATUS_PENDING_VERIFICATION = 'pending-verification'
    STATUS_ACTIVE = 'active'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_PENDING_VERIFICATION, STATUS_ACTIVE, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useremail_user')
    role = models.CharField(max_length=20, default=ROLE_PRIMARY)
    status = models.CharField(max_length=30, default=STATUS_PENDING_VERIFICATION)
    email = models.EmailField()
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='useremail_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPhone(models.Model):
    """ This model is used to store user phone numbers. """
    ROLE_PRIMARY = 'primary'
    ROLE_SECONDARY = 'secondary'
    ROLE_MOBILE = 'mobile'
    ROLE_HOME = 'home'
    ROLE_WORK = 'work'
    ROLE_OTHER = 'other'
    ROLE_NOTIFICATIONS = 'notifications'
    ROLES = [ROLE_PRIMARY, ROLE_SECONDARY, ROLE_MOBILE, ROLE_HOME, ROLE_WORK, ROLE_OTHER, ROLE_NOTIFICATIONS]

    STATUS_PENDING_VERIFICATION = 'pending-verification'
    STATUS_ACTIVE = 'active'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_PENDING_VERIFICATION, STATUS_ACTIVE, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userphone_user')
    role = models.CharField(max_length=20, default=ROLE_PRIMARY)
    status = models.CharField(max_length=30, default=STATUS_PENDING_VERIFICATION)
    phone = models.CharField(max_length=15)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='userphone_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserAddress(models.Model):
    """ This model is used to store user postal addresses. """
    ROLE_PRIMARY = 'primary'
    ROLE_SECONDARY = 'secondary'
    ROLE_HOME = 'home'
    ROLE_WORK = 'work'
    ROLE_OTHER = 'other'
    ROLE_BILLING = 'billing'
    ROLE_SHIPPING = 'shipping'
    ROLES = [ROLE_PRIMARY, ROLE_SECONDARY, ROLE_HOME, ROLE_WORK, ROLE_OTHER, ROLE_BILLING, ROLE_SHIPPING]

    STATUS_ACTIVE = 'active'
    STATUS_DELETED = 'deleted'
    STATUSES = [STATUS_ACTIVE, STATUS_DELETED]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useraddress_user')
    role = models.CharField(max_length=20, default=ROLE_PRIMARY)
    status = models.CharField(max_length=30, default=STATUS_ACTIVE)
    house_number = models.CharField(max_length=10)
    street_pre_directional = models.CharField(max_length=2, null=True)
    street_name = models.CharField(max_length=50)
    street_suffix = models.CharField(max_length=4, null=True)
    street_post_directional = models.CharField(max_length=2, null=True)
    unit_type = models.CharField(max_length=4, null=True)
    unit_number = models.CharField(max_length=10, null=True)
    line1 = models.CharField(max_length=100, null=True)
    line2 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='useraddress_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
