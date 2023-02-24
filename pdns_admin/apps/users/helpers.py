from allauth.account import app_settings
from allauth.account.models import EmailAddress
from django.conf import settings


def require_email_confirmation():
    return settings.ACCOUNT_EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY


def user_has_confirmed_email_address(user, email):
    try:
        email_obj = EmailAddress.objects.get_for_user(user, email)
        return email_obj.verified
    except EmailAddress.DoesNotExist:
        return False
