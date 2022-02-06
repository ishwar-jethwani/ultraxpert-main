# Generated by Django 3.2.5 on 2022-02-03 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20220123_1808'),
        ('meet', '0002_meeting_expert'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.services', verbose_name='Service Name'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='service_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='service_name'),
        ),
    ]