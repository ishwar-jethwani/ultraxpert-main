from django.db import models
from events.models import EventScheduleTime

from user.models import Profile, Services, User
from .utils import *
from django.db.models.signals import pre_save

class Meeting(models.Model):
        meeting_id = models.CharField(max_length=20,verbose_name="Meeting ID",unique=True,blank=True)
        user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
        service = models.ForeignKey(Services,on_delete=models.CASCADE,verbose_name="Service",blank=True,null=True)
        expert = models.ForeignKey(Profile,on_delete=models.CASCADE,verbose_name="Expert",blank=True,null=True)
        event = models.ForeignKey(EventScheduleTime,on_delete=models.CASCADE,verbose_name="Meeteing Event",blank=True,null=True)
        service_name = models.CharField(max_length=100,verbose_name="service_name",blank=True,null=True)
        date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)

        class Meta:
            ordering = ["-date_time"]

        def __str__(self):
            return self.meeting_id




def pre_save_create_meeting_id(sender, instance, *args, **kwargs):
    if not instance.meeting_id:
        instance.meeting_id= unique_meeting_id_generator(instance)
pre_save.connect(pre_save_create_meeting_id, sender=Meeting)  

