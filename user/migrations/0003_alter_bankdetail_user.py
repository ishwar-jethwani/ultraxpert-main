# Generated by Django 3.2.5 on 2022-02-11 04:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_bankdetail_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdetail',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
