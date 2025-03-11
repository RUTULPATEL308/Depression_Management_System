from django.db import models
from django.contrib.auth.models import User  # Using Django's built-in User model
# Create your models here.
from django.utils.timezone import now

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
