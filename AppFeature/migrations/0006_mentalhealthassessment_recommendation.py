# Generated by Django 5.1.6 on 2025-03-14 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFeature', '0005_mentalhealthassessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentalhealthassessment',
            name='recommendation',
            field=models.TextField(blank=True, help_text='AI-generated recommendation', null=True),
        ),
    ]
