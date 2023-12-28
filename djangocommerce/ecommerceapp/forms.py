from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile 

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=60, label='Full Name')
    username = forms.CharField(max_length=30, label='Username')

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'address', 'phone_number', 'date_of_birth', 'profile_image']
