# Generated by Django 3.2.5 on 2022-03-11 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0011_meeting_refunded'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='rated',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Rated'),
        ),
    ]