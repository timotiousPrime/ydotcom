# Models
from django.contrib.auth.models import User
from .models import UserProfile, EmploymentHistory
# Forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import inlineformset_factory


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('title', 'date_of_birth', 'phone_number', 'interests' )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'interests': forms.CheckboxSelectMultiple
        }


class EmploymentHistoryForm(forms.ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = ('start_date', 'end_date', 'organisation_name', 'position')
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'}),
            'position': forms.CheckboxSelectMultiple(),
        }


# Define formset so I can manage multiple employment history records relative to a single user
EmploymentHistoryFormSet = inlineformset_factory(
    UserProfile, EmploymentHistory, 
    form = EmploymentHistoryForm,
    extra=1, can_delete=True
)