# Generated by Django 3.2.5 on 2021-12-29 04:15

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='username')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_joined')),
                ('is_expert', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='user.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'unique_together': {('slug', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Keyword')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='UserPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.CharField(blank=True, max_length=20, unique=True, verbose_name='plan_id')),
                ('plan_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Plan Name')),
                ('plan_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price')),
                ('no_of_service', models.PositiveIntegerField(blank=True, default=5, null=True, verbose_name='No of service which can we add')),
                ('no_of_meeting', models.PositiveBigIntegerField(blank=True, default=2, null=True, verbose_name='No of Meetings')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('expire_in_days', models.PositiveIntegerField(blank=True, default=30, null=True, verbose_name='User plan expire in days')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(blank=True, max_length=100, null=True, verbose_name='icon')),
                ('plateform_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Plateform Name')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Link')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(blank=True, max_length=20, unique=True, verbose_name='Service ID')),
                ('service_type', models.CharField(blank=True, choices=[('duration based service', 'duration based service'), ('delivery based service', 'delivery based service')], max_length=50, null=True, verbose_name='Service Type')),
                ('service_img', models.URLField(blank=True, null=True)),
                ('service_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Service in brief')),
                ('duration', models.CharField(blank=True, max_length=10, null=True, verbose_name='Duration')),
                ('delivery_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Price')),
                ('currency', models.CharField(blank=True, choices=[('INR', 'INR'), ('USD', 'USD'), ('GBP', 'GBP')], default='INR', max_length=10, null=True, verbose_name='Currency')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('tags', models.CharField(blank=True, max_length=200, null=True, verbose_name='Keywords')),
                ('ordered', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=25, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=25, null=True, verbose_name='Last Name')),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('is_online', models.BooleanField(default=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Expert brief')),
                ('profile_img', models.URLField(blank=True)),
                ('education', models.JSONField(blank=True, default=dict, null=True, verbose_name='Education')),
                ('experience', models.JSONField(blank=True, default=dict, null=True, verbose_name='Experience')),
                ('categories', models.ManyToManyField(blank=True, to='user.Category')),
                ('got_projects', models.ManyToManyField(blank=True, related_name='Project_Request', to='activity.Project_Request')),
                ('keywords', models.ManyToManyField(blank=True, to='user.Keywords')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userplans')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder', models.CharField(blank=True, max_length=100, null=True, verbose_name='Account Holder Name')),
                ('bank_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Bank Name')),
                ('account_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Account_number')),
                ('ifsc_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='IFSC Code')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creted On')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
