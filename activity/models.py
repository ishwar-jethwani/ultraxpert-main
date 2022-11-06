from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey
from ckeditor.fields import RichTextField
from rest_framework import status
from events.models import EventScheduleTime
from meet.models import Meeting
from user.models import User,Profile,Services
from django.core.validators import  MaxValueValidator
from .utils import *
from django.db.models.signals import pre_save
from user.models import *

#Project Model
class Project_Request(models.Model):
    """Model For Request Details For Project"""
    request_id = models.CharField(max_length=10,blank=True,unique=True)
    request_from_user = ForeignKey(User,on_delete=models.CASCADE)
    service = ForeignKey(Services,on_delete=models.CASCADE)
    request_to_profile = ForeignKey(Profile,on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.request_id
    
    class Meta:
        ordering = ["-request_time"]

#Pre Saving Reqeust Id
def pre_save_create_request_id(sender, instance, *args, **kwargs):
    if not instance.request_id:
        instance.request_id= unique_request_id_generator(instance)


pre_save.connect(pre_save_create_request_id, sender=Project_Request)

#Ratings Model
class Ratings(models.Model):
    """Model For Ratings Details"""
    user_name = models.ForeignKey(User,on_delete=models.CASCADE)
    short_title = models.CharField(max_length=100,blank=True,null=True)
    review =  RichTextField(blank=True,null=True)
    star_rating = models.PositiveIntegerField(verbose_name="Start Rating",validators=[MaxValueValidator(5)],null=True)
    rating_on = models.ForeignKey(Profile,on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,verbose_name="Created Date",blank=True,null=True)

    def __str__(self) -> str:
        return self.user_name.username+" - "+self.meeting
    
    class Meta:
        ordering = ["pk"]

#Order Model   
class Order(models.Model):
    """Model For order Details"""
    stages = (
        ("pending","pending"),
        ("booked","booked"),
        ("cancelled","cancelled")

    )
    order_id = models.CharField(max_length=10,verbose_name="Order Id",unique=True,blank=True)
    razorpay_order_no = models.CharField(max_length=200,verbose_name="RazorPay Order Number",blank=True,null=True)
    user = models.ForeignKey(User,verbose_name="User",on_delete=models.CASCADE)
    order_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    service_id = models.CharField(max_length=100,verbose_name="Service ID",blank=True,null=True)
    slot = models.ForeignKey(EventScheduleTime,null=True,blank=True,on_delete=models.CASCADE)
    service_obj = models.ForeignKey("user.Services",related_name="Services",on_delete=models.CASCADE,null=True)
    price  = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Price",blank=True)
    order_on = models.ForeignKey("user.User",related_name="User",verbose_name="username",on_delete=models.CASCADE)
    paid = models.BooleanField(default=False,blank=True,null=True)
    status = models.CharField(max_length=50,choices=stages,default="pending",blank=True,null=True)

    def __str__(self) -> str:
        return str(self.order_id)
    class Meta:
        ordering = ["-order_created"]

#Pre Saving Order Id 
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)

#Subscription Model
class Subscriptions(models.Model):
    """Model For Subscription Details"""
    subs_id = models.CharField(max_length=20,verbose_name="id",blank=True)
    plan = models.ForeignKey(UserPlans,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    paid = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self) -> str:
        return self.subs_id

    class Meta:
        ordering = ["-date_created"]

#Pre Saving Subscription Id 
def pre_save_create_subs_id(sender, instance, *args, **kwargs):
    if not instance.subs_id:
        instance.subs_id= unique_subs_id_generator(instance)


pre_save.connect(pre_save_create_subs_id, sender=Subscriptions)