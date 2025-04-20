
from django import forms
from django.contrib.auth.models import User
from AppFeature.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from AppFeature.models import BookAppointment, MentalHealthAssessment
from django.forms import ModelForm



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

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = BookAppointment
        fields = ['provider', 'appointment_date', 'time', 'reason']
        widgets = {
            'provider': forms.Select(choices=[
                ('', 'Select Provider'),
                ('Dr. Smith', 'Dr. Smith'),
                ('Dr. Johnson', 'Dr. Johnson'),
                ('Dr. Brown', 'Dr. Brown'),
                ('Dr. Taylor', 'Dr. Taylor'),
                ('Dr. Williams', 'Dr. Williams')
            ], attrs={'class': 'form-control'}),

            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True, user=None):
        appointment = super().save(commit=False)
        if user:
            appointment.user = user  # Assign the logged-in user to the appointment
        if commit:
            appointment.save()
        return appointment

class MentalHealthAssessmentForm(forms.ModelForm):
    class Meta:
        model = MentalHealthAssessment
        fields = ['emotional_state', 'sleep_hours', 'sleep_quality', 'appetite_changes', 'energy_levels', 'interest_in_activities', 'social_engagement', 'suicidal_thoughts']
        widgets = {
                    # 'mood_level': forms.NumberInput(attrs={'class': 'form-control', 'style': 'background: linear-gradient(to right, #ff0000, #ffff00, #00ff00); height: 5px;', 'type': 'range', 'min': '1', 'max': '10', 'step': '1'}),
                    'emotional_state': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
                    'sleep_hours': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;', 'step': '0.5'}),
                    'sleep_quality': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
                    'appetite_changes': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
                    'energy_levels': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
                    'interest_in_activities': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
                    'social_engagement': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
                    'suicidal_thoughts': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'font-size: 14px;'}),
                }

from django import forms

class EmailOrUsernameLoginForm(forms.Form):
    username = forms.CharField(
        label="Username or Email", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
