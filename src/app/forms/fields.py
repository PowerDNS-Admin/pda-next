from django import forms
from django.contrib.auth.forms import UsernameField as BaseUsernameField
from django.utils.translation import gettext_lazy as _
from app.forms.widgets import EmailInput, NumberInput, CheckboxInput, UsernameInput, UsernameOrEmailInput, \
    PasswordInput, Input, TextInput, FirstNameWidget, LastNameWidget

base_attrs = {
    'class': 'form-control',
    'autocapitalize': 'none',
    'autocorrect': 'off',
    'spellcheck': 'false',
}


class InputField(forms.CharField):
    widget = Input(attrs=base_attrs)


class CharField(forms.CharField):
    widget = TextInput(attrs=base_attrs)


class IntegerField(forms.IntegerField):
    widget = NumberInput(attrs={**base_attrs, 'autocomplete': 'number', 'maxlength': 10, 'placeholder': 'Number'})
    default_error_messages = {
        'invalid': _('Please enter a whole number.'),
    }


class CheckboxField(InputField):
    widget = CheckboxInput(attrs={**base_attrs, 'label': 'Yes'})


class EmailField(forms.EmailField):
    required = True
    widget = EmailInput(attrs={**base_attrs, 'autocomplete': 'email', 'maxlength': 150, 'placeholder': 'Email Address'})


class FirstNameField(CharField):
    label = _('First / Given Name')
    required = True
    widget = FirstNameWidget(
        attrs={**base_attrs, 'autocomplete': 'given-name', 'maxlength': 30, 'placeholder': 'First / Given Name'})


class LastNameField(CharField):
    label = _('Last / Family Name')
    required = True
    widget = LastNameWidget(
        attrs={**base_attrs, 'autocomplete': 'family-name', 'maxlength': 50, 'placeholder': 'Last / Family Name'})


class NewPasswordField(CharField):
    label = _('Password')
    strip = False
    widget = PasswordInput(
        attrs={**base_attrs, 'autocomplete': 'new-password', 'maxlength': 254, 'placeholder': 'Password'})


class NewPasswordConfirmField(CharField):
    label = _('Confirm Password')
    strip = False
    widget = PasswordInput(
        attrs={**base_attrs, 'autocomplete': 'new-password', 'maxlength': 254, 'placeholder': 'Confirm Password'})


class UsernameField(BaseUsernameField):
    required = True
    widget = UsernameInput(
        attrs={**base_attrs, 'autocomplete': 'username', 'autofocus': True, 'maxlength': 150,
               'placeholder': 'Username'})


class UsernameOrEmailField(BaseUsernameField):
    required = True
    widget = UsernameOrEmailInput(
        attrs={**base_attrs, 'autocomplete': 'username', 'autofocus': True, 'maxlength': 150,
               'placeholder': 'Username or Email Address'})


class PasswordField(forms.CharField):
    label = _('Password')
    strip = False
    widget = PasswordInput(
        attrs={**base_attrs, 'autocomplete': 'password', 'maxlength': 254, 'placeholder': 'Password'})
