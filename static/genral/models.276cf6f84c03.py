from django.db import models
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField

class AboutUs(models.Model):
    title = models.CharField(max_length=150,verbose_name="Title",null=True,blank=True)
    description  = RichTextField(blank=True,null=True,verbose_name="Description")
    social_media_handle = models.JSONField(null=True,blank=True,verbose_name="Social Media")
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name="Upload Date")
    support_number = PhoneNumberField(blank=True,null=True,verbose_name="Support Conatct Number")
    number = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["number"]

class Banner(models.Model):
    title = models.CharField(max_length=150,verbose_name="Title",null=True,blank=True)
    banner = models.JSONField(null=True,blank=True,verbose_name="Banner Json")
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name="Upload Date")
    number = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["number"]
    
class SupportQuery(models.Model):
    name =  models.CharField(max_length=150,verbose_name="Name",null=True,blank=True)
    contact_number = PhoneNumberField(blank=True,null=True,verbose_name="Conatct Number")
    email = models.EmailField(blank=True,null=True)
    subject = models.CharField(max_length=200,verbose_name="Subject",null=True,blank=True)
    message = RichTextField(null=True,blank=True,verbose_name="Message")
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name="Date")
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date_created"]

class Blog(models.Model):
    title = models.CharField(max_length=150,verbose_name="Title",null=True,blank=True)
    content = RichTextField(blank=True,null=True,verbose_name="Content")
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name="Date")
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_created"]

