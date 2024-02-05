from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from app.forms.fields import UsernameField


class PasswordResetForm(forms.Form):

    _request: HttpRequest
    """The HttpRequest object associated with this form."""

    username = UsernameField()

    def send_mail(
            self,
            from_email,
            to_email,
            context,
            subject_template_name,
            text_email_template_name,
            html_email_template_name,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        from django.template import loader
        from apps.notifications.lib import NotificationManager
        from apps.notifications.models import Notification
        from apps.notifications.tasks import send_notification

        if 'site_name' in context:
            site_name = context['site_name']
        else:
            from django.contrib.sites.shortcuts import get_current_site
            current_site = get_current_site(self._request)
            site_name = current_site.name

        # Load email subject from template
        subject = loader.render_to_string(subject_template_name, context)
        # Remove newlines within subject
        subject = "".join(subject.splitlines())

        # Load email body from templates
        body_text = loader.render_to_string(text_email_template_name, context)
        body_html = None

        if html_email_template_name is not None:
            # Load email HTML body from template
            body_html = loader.render_to_string(html_email_template_name, context)

        params = {
            'label': f'{site_name} User Password Reset',
            'notification_format': Notification.FORMAT_EMAIL,
            'created_by': None,
            'urgent': True,
        }

        notification = NotificationManager.create(**params)
        notification.save()

        email_params = {
            'from_email': from_email,
            'subject': subject,
            'text_body': body_text,
            'html_body': body_html,
        }

        email = NotificationManager.create_email(notification, **email_params)
        email.save()

        recipient = NotificationManager.create_email_recipient(notification, to_email)
        recipient.save()

        # Schedule the notification for immediate sending
        send_notification.delay(notification.pk)

    def get_users(self, username_or_email):
        """Given a username or email address, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        from django.contrib.auth import get_user_model
        from django.contrib.auth.forms import _unicode_ci_compare
        from django.db.models import Q

        UserModel = get_user_model()

        email_field_name = UserModel.get_email_field_name()
        username_field_name = 'username'

        active_users = UserModel._default_manager.filter(
            Q(**{"%s__iexact" % email_field_name: username_or_email, "is_active": True})
            | Q(**{"%s__iexact" % username_field_name: username_or_email, "is_active": True})
        )

        return (
            u
            for u in active_users
            if u.has_usable_password()
               and (_unicode_ci_compare(username_or_email, getattr(u, email_field_name))
                    or _unicode_ci_compare(username_or_email, getattr(u, username_field_name)))
        )

    def save(
            self,
            from_email=None,
            request=None,
            extra_email_context=None,
            subject_template_name='user/password/reset_email_subject.jinja2',
            text_email_template_name='user/password/reset_email_text.jinja2',
            html_email_template_name='user/password/reset_email_html.jinja2',
            token_generator=default_token_generator,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        from django.contrib.auth import get_user_model
        from django.contrib.sites.shortcuts import get_current_site
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        from app import config

        UserModel = get_user_model()

        self._request = request
        username_or_email = self.cleaned_data['username']
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(username_or_email):
            user_email = getattr(user, email_field_name)
            context = {
                'domain': domain,
                'port': config.web.port().ref,
                'protocol': config.web.protocol().ref,
                'site_name': site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                **(extra_email_context or {}),
            }
            self.send_mail(
                from_email,
                user_email,
                context,
                subject_template_name,
                text_email_template_name,
                html_email_template_name,
            )
