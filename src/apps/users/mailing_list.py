from django.conf import settings

try:
    from mailchimp3 import MailChimp
    from mailchimp3.mailchimpclient import MailChimpError

    MAILCHIMP_AVAILABLE = True
except ImportError:
    MAILCHIMP_AVAILABLE = False


def get_mailchimp_client():
    if getattr(settings, "MAILCHIMP_API_KEY", None) and getattr(settings, "MAILCHIMP_LIST_ID", None):
        return MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
    else:
        return None


def is_mailchimp_available():
    return MAILCHIMP_AVAILABLE and get_mailchimp_client() is not None


def subscribe_to_mailing_list(email_address):
    if not is_mailchimp_available():
        return

    try:
        get_mailchimp_client().lists.members.create(
            settings.MAILCHIMP_LIST_ID,
            {
                "email_address": email_address,
                "status": "subscribed",
            },
        )
    except MailChimpError as e:
        # likely it's just that they were already subscribed so don't worry about it
        try:
            # but do log to sentry if available
            from sentry_sdk import capture_exception

            capture_exception(e)
        except ImportError:
            pass
