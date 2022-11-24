from django.db import models
from user.models import *
from .utils import *

class Training(models.Model):
    training_id = models.CharField(max_length=20,verbose_name="Trininig ID",blank=True,null=True)
    training_name = models.CharField(max_length=100,verbose_name="Training Name",blank=True,null=True)
    technology =  models.CharField(max_length=100,verbose_name="Technology",blank=True,null=True)
    duration = models.DurationField(default=0,verbose_name="Duration",blank=True,null=True)
    parent = models.ForeignKey("self",on_delete=models.CASCADE,verbose_name="Parent Category")
    created_on = models.DateTimeField(auto_now_add=True,verbose_name="Training Created On",blank=True,null=True)

    def __str__(self) -> str:
        return self.training_name

    class Meta:
        ordering = ["-created_on"]

def pre_save_create_taining_id(sender, instance, *args, **kwargs):
    if not instance.training_id:
        instance.training_id = unique_training_id_generator(instance)
pre_save.connect(pre_save_create_taining_id, sender=Services)


class Company(models.Model):
    company_id = models.CharField(max_length=20,verbose_name="Company ID",blank=True,null=True)
    name = models.CharField(max_length=500,verbose_name="Compnay Name",blank=True,null=True)
    registration_no = models.CharField(max_length=100,verbose_name="Registration Number",blank=True,null=True)
    company_address = models.JSONField(default=dict,verbose_name="address",blank=True,null=True)
    no_of_employees = models.PositiveIntegerField(default=0,verbose_name="No Of Employees")
    created_on = models.DateTimeField(auto_now_add=True,verbose_name="Registered On",blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,verbose_name="Renewed On",blank=True,null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ["-created_on"]

def pre_save_create_company_id(sender, instance, *args, **kwargs):
    if not instance.company_id:
        instance.company_id = unique_company_id_generator(instance)
pre_save.connect(pre_save_create_company_id, sender=Services)

class Employee(models.Model):
    employee_id = models.CharField(max_length=10,verbose_name="Employee ID",blank=True,null=True)
    employee_name = models.CharField(max_length=200,verbose_name="Employee Full Name",blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="Employee Details")
    employee_address = models.JSONField(default=dict,verbose_name="Employee Full Address",blank=True,null=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="Company Name")
    joined_on = models.DateField(auto_now_add=True,verbose_name="Joined On",blank=True,null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ["-created_on"]

def pre_save_create_employee_id(sender, instance, *args, **kwargs):
    if not instance.employee_id:
        instance.employee_id = unique_employee_id_generator(instance)
pre_save.connect(unique_employee_id_generator, sender=Services)



