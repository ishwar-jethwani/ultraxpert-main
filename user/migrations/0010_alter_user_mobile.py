# Generated by Django 3.2.5 on 2022-01-23 07:53

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20220118_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
    ]
