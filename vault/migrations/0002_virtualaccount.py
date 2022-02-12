# Generated by Django 3.2.5 on 2022-02-11 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('virual_account_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Virtual Account ID')),
                ('virual_data', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]