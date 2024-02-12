# Models
from django.contrib.auth.models import User

# Forms
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=24, strip=True, required=True)
    last_name = forms.CharField(max_length=24, strip=True, required=True)
    class meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']