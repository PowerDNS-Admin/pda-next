from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.forms.fields import (
    CheckboxField, UsernameField, NewPasswordField, NewPasswordConfirmField, EmailField, FirstNameField, LastNameField
)
from app.forms.widgets import CheckboxInput


class RegistrationForm(UserCreationForm):
    first_name = FirstNameField()
    last_name = LastNameField()
    email = EmailField()
    username = UsernameField()
    password1 = NewPasswordField()
    password2 = NewPasswordConfirmField()
    terms = CheckboxField(widget=CheckboxInput(attrs={'label': 'I agree to the terms of use.'}))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
