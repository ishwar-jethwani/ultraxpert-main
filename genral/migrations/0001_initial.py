# Generated by Django 3.2.5 on 2022-11-01 03:29

import ckeditor.fields
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('social_media_handle', models.JSONField(blank=True, null=True, verbose_name='Social Media')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Upload Date')),
                ('support_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Support Conatct Number')),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True, verbose_name='Title')),
                ('banner', models.JSONField(blank=True, null=True, verbose_name='Banner Json')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Upload Date')),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True, verbose_name='Title')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Content')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='SupportQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name')),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Conatct Number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subject', models.CharField(blank=True, max_length=200, null=True, verbose_name='Subject')),
                ('message', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Message')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
