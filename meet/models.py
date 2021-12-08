from django.db import models

from user.models import Services, User
from .utils import *
from django.db.models.signals import pre_save

class Meeting(models.Model):
        meeting_id = models.CharField(max_length=20,verbose_name="Meeting ID",unique=True,blank=True)
        date_time = models.DateTimeField(verbose_name="Date and Time of Meeting Creaton",auto_now_add=True)
        expert = models.ForeignKey(User,on_delete=models.PROTECT)
        service_name = models.CharField(max_length=200,verbose_name="Service Name",blank=True)

        class Meta:
            ordering = ["-date_time"]

        def __str_(self):
            self.meeting_id


def pre_save_create_meeting_id(sender, instance, *args, **kwargs):
    if not instance.meeting_id:
        instance.meeting_id= unique_meeting_id_generator(instance)
pre_save.connect(pre_save_create_meeting_id, sender=Meeting)  

