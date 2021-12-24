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
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]
    
    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser,PermissionsMixin):
    user_id     = models.CharField(max_length=10,unique=True)
    username    = models.CharField(max_length=50,unique=True,verbose_name="username")
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_active   = models.BooleanField(('active'), default=True)
    mobile      = PhoneNumberField()
    email       = models.EmailField(('email address'),unique=True)
    date_joined = models.DateTimeField(('date_joined'), auto_now_add=True)
    is_expert   = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')




class User_Plans(models.Model):
    plan_id         = models.CharField(max_length=20,verbose_name="plan_id",blank=True,unique=True)
    plan_name       = models.CharField(max_length=50,verbose_name="Plan Name")
    plan_price      = models.DecimalField(verbose_name="Price",decimal_places=2,max_digits=10)
    no_of_service   = models.PositiveIntegerField(default=5,verbose_name="No of service which can we add")
    no_of_meeting   = models.PositiveBigIntegerField(default=2,verbose_name="No of Meetings")
    date_created    = models.DateField(auto_now_add=True)
    expire_in_days  = models.PositiveIntegerField(default=30,verbose_name="User plan expire in days")


    def __str__(self) -> str:
        return self.plan_name
    
    class Meta:
        ordering = ["pk"]



class SocialMedia(models.Model):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    icon    = models.CharField(max_length=100,verbose_name="icon")
    plateform_name = models.CharField(max_length=30,verbose_name="Plateform Name")
    link    = models.URLField(verbose_name="Link")


    def __str__(self) -> str:
        return self.link


Services_type = (
    ("duration based service","duration based service"),
    ("delivery based service","delivery based service")
)
class Category(models.Model):
    name    = models.CharField(max_length=200)
    slug    = models.SlugField()
    parent  = models.ForeignKey('self',blank=True, null=True ,related_name='children',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

class Services(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    service_id      = models.CharField(max_length=20,verbose_name="Service ID",unique=True,blank=True)
    service_type    = models.CharField(max_length=50,verbose_name="Service Type",choices=Services_type)
    service_img     = models.URLField(blank=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    service_name    = models.CharField(max_length=100,verbose_name="Title")
    description     = RichTextField(verbose_name="Service in brief")
    duration        = models.CharField(max_length=10,verbose_name="Duration",blank=True,null=True)
    delivery_date   = models.DateTimeField(blank=True,default=timezone.now)
    price           = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Price",blank=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    tags            = models.CharField(max_length=200,verbose_name="Keywords")
    ordered         = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.service_name

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)

    class Meta:
        ordering= ["-date_created"]





class Profile(models.Model):
    first_name          = models.CharField(max_length=25,verbose_name="First Name")
    last_name           = models.CharField(max_length=25,verbose_name="Last Name")
    profile             = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number       = PhoneNumberField(blank=True,null=True)
    is_online           = models.BooleanField(default=False)
    got_projects        = models.ManyToManyField("activity.Project_Request",related_name="Project_Request",blank=True)
    title               = models.CharField(max_length=100,verbose_name="Title")
    description         = RichTextField(verbose_name="Expert brief")
    profile_img         = models.URLField(blank=True)
    keywords            = models.ManyToManyField(Keywords,blank=True)
    categories          = models.ManyToManyField(Category,blank=True)
    user_plan           = models.ForeignKey(User_Plans,on_delete=models.CASCADE,null=True)
    education           = models.JSONField(default=dict,verbose_name="Education")
    experience          = models,JSONField(default=dict,verbose_name="Experience")




    def __str__(self) -> str:
        return self.profile.username

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
    pass


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


pre_save.connect(pre_save_create_plan_id, sender=User_Plans)































def pre_save_create_user_id(sender, instance, *args, **kwargs):
    if not instance.user_id:
        instance.user_id= unique_user_id_generator(instance)
        
pre_save.connect(pre_save_create_user_id, sender=User)


