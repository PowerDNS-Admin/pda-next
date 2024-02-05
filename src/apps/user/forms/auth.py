from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import gettext_lazy as _
from app.forms.fields import UsernameField, PasswordField


class AuthenticationForm(BaseAuthenticationForm):
    username = UsernameField()
    password = PasswordField()

    default_error_messages = {
        'invalid_login': _('Please enter a correct %(username)s and password. '
                           + 'Note that these fields may be case-sensitive.'),
        'inactive': _('Your user profile is currently disabled. Please contact customer support.'),
    }
