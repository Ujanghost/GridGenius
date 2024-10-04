# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=60, label="Full Name")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        full_name = self.cleaned_data['full_name']

        # Safely handle full_name split
        if ' ' in full_name:
            first_name, last_name = full_name.split(' ', 1)
        else:
            first_name = full_name
            last_name = ''  # Set last name as an empty string if not provided

        user.first_name = first_name
        user.last_name = last_name

        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
