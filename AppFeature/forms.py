
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

class AppointmentForm(ModelForm):
    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter patient name', 'style': 'font-size: 14px;','value':'Hetali', 'readonly':'readonly'}))
    provider = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter provider name', 'style': 'font-size: 14px;'}))
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter appointment date', 'style': 'font-size: 14px;', 'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter appointment time', 'style': 'font-size: 14px;', 'type': 'time'}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter reason for appointment', 'rows': 2, 'style': 'font-size: 14px;'}))
    # status = forms.ChoiceField(
    #     choices=[('', 'Select Status'), ('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Canceled', 'Canceled')],
    #     widget=forms.Select(attrs={'class': 'form-control form-control-lg','style': 'font-size: 14px;'})
    #     )
    class Meta:
        model = BookAppointment
        fields = ['user', 'provider', 'appointment_date', 'time', 'reason']
    
        


class MentalHealthAssessmentForm(forms.ModelForm):
    class Meta:
        model = MentalHealthAssessment
        fields = ['mood_level', 'emotional_state', 'sleep_hours', 'sleep_quality', 'appetite_changes', 'energy_levels', 'interest_in_activities', 'social_engagement', 'suicidal_thoughts']
        widgets = {
            'mood_level': forms.Select(choices=[(i, str(i)) for i in range(1, 11)], attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
            'emotional_state': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;', 'step': '0.5'}),
            'sleep_quality': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
            'appetite_changes': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
            'energy_levels': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
            'interest_in_activities': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
            'social_engagement': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 14px;'}),
            'suicidal_thoughts': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'font-size: 14px;'}),
        }
