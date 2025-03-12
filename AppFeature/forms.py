
from django import forms
from django.contrib.auth.models import User
from AppFeature.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))  # Ensure email is mandatory
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))  # Password field
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))  # Confirm password field
    
    class Meta:
        model = User  # Using Django's built-in User model
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']  # Fields to be displayed in the form

        widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Lastname'}),
             }

