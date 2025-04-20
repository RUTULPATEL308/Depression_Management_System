from django.contrib.auth.models import User  # Using Django's built-in User model
# Create your models here.
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from threading import local


class SymptomLog(models.Model):
    """
    Stores daily symptom tracking for a patient.
    """
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('neutral', 'Neutral'),
        ('anxious', 'Anxious'),
        ('depressed', 'Depressed'),
        ('stressed', 'Stressed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')
    sleep_hours = models.FloatField(help_text="Number of hours slept")
    physical_activity = models.PositiveIntegerField(help_text="Minutes of exercise", default=0)
    appetite = models.CharField(max_length=50, help_text="Changes in appetite")
    energy_levels = models.IntegerField(help_text="Scale: 1 (Low) - 10 (High)")
    additional_notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.patient.username} - {self.mood} on {self.timestamp.date()}"

    class Meta:
        ordering = ['-timestamp']


class WearableData(models.Model):
    """
    Stores data from wearable devices like heart rate and sleep tracking.
    """
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    heart_rate = models.PositiveIntegerField(help_text="Heart Rate in BPM")
    step_count = models.PositiveIntegerField(help_text="Steps walked today")
    sleep_quality = models.CharField(max_length=50, help_text="Good, Moderate, Poor")
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.patient.username} - {self.heart_rate} BPM on {self.timestamp.date()}"

    class Meta:
        ordering = ['-timestamp']


class AIRecommendation(models.Model):
    """
    Stores AI-generated recommendations based on mood and symptom tracking.
    """
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom_log = models.ForeignKey(SymptomLog, on_delete=models.CASCADE)
    recommendation = models.TextField(help_text="AI-generated suggestion")
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Recommendation for {self.patient.username} on {self.timestamp.date()}"

    class Meta:
        ordering = ['-timestamp']

class CustomUser(models.Model):
    """
    Custom user model extending Django's built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from threading import local

_thread_locals = local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class BookAppointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    provider = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled')
        ],
        default='scheduled'
    )
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Appointment for {self.patient.username} with {self.provider} on {self.appointment_date}"



class MentalHealthAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood_level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    emotional_state = models.CharField(
        max_length=20, 
        choices=[("Happy", "Happy"), ("Sad", "Sad"), ("Anxious", "Anxious"), ("Stressed", "Stressed")]
    )
    sleep_hours = models.FloatField()
    sleep_quality = models.CharField(
        max_length=20, 
        choices=[("Good", "Good"), ("Average", "Average"), ("Poor", "Poor")]
    )
    appetite_changes = models.CharField(
        max_length=20, 
        choices=[("Increase", "Increase"), ("Decrease", "Decrease"), ("Normal", "Normal")]
    )
    energy_levels = models.CharField(
        max_length=20, 
        choices=[("Low", "Low"), ("Normal", "Normal"), ("High", "High")]
    )
    interest_in_activities = models.CharField(
        max_length=20, 
        choices=[("Normal", "Normal"), ("Decreased", "Decreased"), ("Lost", "Lost")]
    )
    social_engagement = models.CharField(
        max_length=20, 
        choices=[("Frequent", "Frequent"), ("Occasional", "Occasional"), ("Isolated", "Isolated")]
    )
    suicidal_thoughts = models.BooleanField(default=False)
    recommendation = models.JSONField(help_text="AI-generated recommendation in JSON format", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

