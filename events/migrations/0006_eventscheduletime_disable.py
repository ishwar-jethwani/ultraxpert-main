# Generated by Django 3.2.5 on 2022-02-14 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_eventscheduletime_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventscheduletime',
            name='disable',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
