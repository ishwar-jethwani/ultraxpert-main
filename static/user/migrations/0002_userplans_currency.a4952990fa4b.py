# Generated by Django 3.2.5 on 2022-02-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplans',
            name='currency',
            field=models.CharField(blank=True, choices=[('INR', 'INR'), ('USD', 'USD'), ('GBP', 'GBP')], default='INR', max_length=10, null=True, verbose_name='Currency'),
        ),
    ]
