# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    contact_no = forms.CharField(max_length=15)
   

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'contact_no', 'password1', 'password2')
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
