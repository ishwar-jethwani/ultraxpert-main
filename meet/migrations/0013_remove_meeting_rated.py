# Generated by Django 3.2.5 on 2022-03-11 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0012_meeting_rated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='rated',
        ),
    ]
