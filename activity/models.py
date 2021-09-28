from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey
from ckeditor.fields import RichTextField
from rest_framework import status
from user.models import User,Profile,Services
from django.core.validators import  MaxValueValidator
from .utils import *
from django.db.models.signals import pre_save
from user.models import *

class Project_Request(models.Model):
    request_id = models.CharField(max_length=10,blank=True,unique=True)
    request_from_user = ForeignKey(User,on_delete=models.CASCADE)
    service = ForeignKey(Services,on_delete=models.CASCADE)
    request_to_profile = ForeignKey(Profile,on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.request_id
    
    class Meta:
        ordering = ["-request_time"]


def pre_save_create_request_id(sender, instance, *args, **kwargs):
    if not instance.request_id:
        instance.request_id= unique_request_id_generator(instance)


pre_save.connect(pre_save_create_request_id, sender=Project_Request)


class Ratings(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE)
    review =  RichTextField()
    star_rating = models.PositiveIntegerField(verbose_name="Start Rating",validators=[MaxValueValidator(5)])
    rating_on = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,verbose_name="Created Date")

    def __str__(self) -> str:
        return self.user_name.username
    
    class Meta:
        ordering = ["pk"]

    
class Order(models.Model):
    stages = (
        ("booked","booked"),
        ("confirmed","confirmed"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),
        ("refunded","refunded"),

    )
    order_id = models.CharField(max_length=10,verbose_name="Order Id",unique=True,blank=True)
    user = models.ForeignKey(User,verbose_name="User",on_delete=models.PROTECT)
    order_created = models.DateTimeField(auto_now_add=True)
    service_id = models.CharField(max_length=100,verbose_name="Service ID")
    service_obj = models.ForeignKey("user.Services",related_name="Services",on_delete=models.CASCADE,null=True)
    price  = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Price",blank=True)
    order_on = models.ForeignKey("user.User",related_name="User",verbose_name="username",on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50,choices=stages,default="booked")

    def __str__(self) -> str:
        return self.order_id


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)

class Subscriptions(models.Model):
    subs_id = models.CharField(max_length=20,verbose_name="id",blank=True)
    plan = models.ForeignKey(User_Plans,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subs_id







def pre_save_create_subs_id(sender, instance, *args, **kwargs):
    if not instance.subs_id:
        instance.subs_id= unique_subs_id_generator(instance)


pre_save.connect(pre_save_create_subs_id, sender=Subscriptions)