from re import T
from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db.models.fields.json import JSONField
from googleapiclient import model
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from .utils import *
from .manager import CustomUserManager
from ckeditor.fields import RichTextField
from django.shortcuts import reverse
import os
from datetime import datetime, timedelta
from django.utils import timezone
import json



class Keywords(models.Model):
    name = models.CharField(max_length=10,verbose_name="Keyword",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    class Meta:
        ordering = ["-date_created"]
    
    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser,PermissionsMixin):
    user_id     = models.CharField(max_length=10,unique=True,blank=True,null=True)
    username    = models.CharField(max_length=50,verbose_name="username",blank=True,null=True)
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_active   = models.BooleanField(('active'), default=True)
    mobile      = PhoneNumberField(blank=True,null=True,unique=True)
    email       = models.EmailField(('email address'),unique=True,blank=True,null=True)
    date_joined = models.DateTimeField(('date_joined'),auto_now_add=True,blank=True,null=True)
    is_expert   = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    objects     = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.user_id

    
    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')




class UserPlans(models.Model):
    plan_id         = models.CharField(max_length=20,verbose_name="plan_id",blank=True,unique=True)
    plan_name       = models.CharField(max_length=50,verbose_name="Plan Name",blank=True,null=True)
    plan_price      = models.DecimalField(verbose_name="Price",decimal_places=2,max_digits=10,blank=True,null=True)
    no_of_service   = models.PositiveIntegerField(default=5,verbose_name="No of service which can we add",blank=True,null=True)
    no_of_meeting   = models.PositiveBigIntegerField(default=0,verbose_name="No of Meetings",blank=True,null=True)
    duration        = models.DurationField(verbose_name="Meeting Duration",blank=True,null=True)
    date_created    = models.DateField(auto_now_add=True,blank=True,null=True)
    expire_in_days  = models.PositiveIntegerField(default=30,verbose_name="User plan expire in days",blank=True,null=True)

    def __str__(self) -> str:
        return self.plan_name
    
    class Meta:
        ordering = ["pk"]



class Category(models.Model):
    name    = models.CharField(max_length=200)
    img     = models.URLField(null=True,blank=True)
    number  = models.PositiveIntegerField(null=True,blank=True)


    class Meta:
        verbose_name_plural = "categories" 
        ordering = ["number"]
    def __str__(self) -> str:
        return self.name


class Services(models.Model):
    currency_take = (
        ("INR","INR"),
        ("USD","USD"),
        ("GBP","GBP")
    )
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    service_id      = models.CharField(max_length=20,verbose_name="Service ID",unique=True,blank=True)
    service_type    = models.CharField(max_length=50,verbose_name="Service Type",blank=True,null=True)
    service_img     = models.URLField(blank=True,null=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    service_name    = models.CharField(max_length=100,verbose_name="Title",blank=True,null=True)
    description     = RichTextField(verbose_name="Service in brief",blank=True,null=True)
    duration        = models.CharField(max_length=10,verbose_name="Duration",blank=True,null=True)
    delivery_date   = models.DateTimeField(blank=True,default=timezone.now)
    price           = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Price",blank=True)
    currency        = models.CharField(max_length=10,verbose_name="Currency",choices=currency_take,default="INR",blank=True,null=True)
    date_created    = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    tags            = models.CharField(max_length=200,verbose_name="Keywords",blank=True,null=True)

    def __str__(self) -> str:
        return self.service_name

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)

    class Meta:
        ordering= ["-date_created"]





class Profile(models.Model):
    gender =(
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other")
    )
    first_name          = models.CharField(max_length=25,verbose_name="First Name",blank=True,null=True)
    last_name           = models.CharField(max_length=25,verbose_name="Last Name",blank=True,null=True)
    profile             = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number       = PhoneNumberField(blank=True,null=True)
    is_online           = models.BooleanField(default=False)
    got_projects        = models.ManyToManyField("activity.Project_Request",related_name="Project_Request",blank=True)
    title               = models.CharField(max_length=100,verbose_name="Title",blank=True,null=True)
    description         = RichTextField(verbose_name="Expert brief",blank=True,null=True)
    profile_img         = models.URLField(blank=True)
    gender              = models.CharField(max_length=10,verbose_name="Gender",choices=gender,blank=True,null=True)
    country             = models.CharField(max_length=100,verbose_name="Country",blank=True,null=True)
    keywords            = models.ManyToManyField(Keywords,blank=True)
    categories          = models.ManyToManyField(Category,blank=True)
    user_plan           = models.ForeignKey(UserPlans,on_delete=models.CASCADE,null=True)
    education           = models.CharField(max_length=1000,verbose_name="Education",blank=True,null=True)
    experience          = models.CharField(max_length=1000,verbose_name="Experience",blank=True,null=True)


    def __str__(self) -> str:
        return self.profile.user_id

    def set_keyword(self, x):
        self.keywords = json.dumps(x)

    def get_keyword(self):
        key = json.loads(self.keywords)
        return key

        
    def get_absolute_url(self):
        return reverse("profile",kwargs={"username":self.profile.username})
    

    class Meta:
        ordering = ["pk"]



class BankDetail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    account_holder = models.CharField(max_length=100,verbose_name="Account Holder Name",blank=True,null=True)
    bank_name = models.CharField(max_length=1000,verbose_name="Bank Name",blank=True,null=True)
    account_number = models.CharField(max_length=20,verbose_name="Account_number",blank=True,null=True)
    ifsc_code = models.CharField(max_length=100,verbose_name="IFSC Code",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Creted On",blank=True,null=True)

    def __str__(self) -> str:
        return self.user.user_id

    class Meta:
        ordering = ["-timestamp"]
    

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    service = models.ForeignKey(Services,on_delete=models.CASCADE,blank=True,null=True)
    comment = models.CharField(max_length=200000,verbose_name="Comment",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    reply = models.ForeignKey("self",related_name="comment_reply",blank=True,null=True,on_delete=models.PROTECT,verbose_name="Reply")

    def __str__(self) -> str:
        return self.user.user_id

    class Meta:
        ordering = ["-timestamp"]






def pre_save_create_user_id(sender, instance, *args, **kwargs):
    if not instance.user_id:
        instance.user_id= unique_user_id_generator(instance)


pre_save.connect(pre_save_create_user_id, sender=User)



def pre_save_create_service_id(sender, instance, *args, **kwargs):
    if not instance.service_id:
        instance.service_id= unique_service_id_generator_service(instance)


pre_save.connect(pre_save_create_service_id, sender=Services)



def pre_save_create_plan_id(sender, instance, *args, **kwargs):
    if not instance.plan_id:
        instance.plan_id= f"PLAN{unique_plan_id_generator(instance)}"


pre_save.connect(pre_save_create_plan_id, sender=UserPlans)































def pre_save_create_user_id(sender, instance, *args, **kwargs):
    if not instance.user_id:
        instance.user_id= unique_user_id_generator(instance)
        
pre_save.connect(pre_save_create_user_id, sender=User)


