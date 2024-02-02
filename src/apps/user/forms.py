from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
	"""docstring for RegistrationForm"""
	from django import forms
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=50, required=True)
	email = forms.EmailField(required=True)
	terms = forms.CheckboxInput()

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

