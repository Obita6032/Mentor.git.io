# Generated by Django 5.1.3 on 2024-11-29 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0004_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]
