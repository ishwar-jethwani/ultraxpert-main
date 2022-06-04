# Generated by Django 3.2.5 on 2022-02-09 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_eventscheduletime_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='discription',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Discription'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Event Name'),
        ),
    ]
