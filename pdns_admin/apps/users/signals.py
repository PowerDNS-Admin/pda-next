from allauth.account.signals import email_confirmed, user_signed_up
from django.conf import settings
from django.core.mail import mail_admins
from django.dispatch import receiver

from apps.users.mailing_list import subscribe_to_mailing_list


@receiver(user_signed_up)
def handle_sign_up(request, user, **kwargs):
    # customize this function to do custom logic on sign up, e.g. send a welcome email
    # or subscribe them to your mailing list.
    # This example notifies the admins, in case you want to keep track of sign ups
    _notify_admins_of_signup(user)
    # and subscribes them to a mailchimp mailing list
    subscribe_to_mailing_list(user.email)


@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    """
    When an email address is confirmed make it the primary email.
    """
    # This also sets user.email to the new email address.
    # hat tip: https://stackoverflow.com/a/29661871/8207
    email_address.set_as_primary()


def _notify_admins_of_signup(user):
    mail_admins(
        f"Yowsers, someone signed up for {settings.PROJECT_METADATA['NAME']}!",
        "Email: {}".format(user.email),
        fail_silently=True,
    )
