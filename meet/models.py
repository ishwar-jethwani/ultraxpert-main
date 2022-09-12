from django.db import models
from events.models import EventScheduleTime

from user.models import Profile, Services, User
from .utils import *
from django.db.models.signals import pre_save

class Meeting(models.Model):
        meeting_id = models.CharField(max_length=20,verbose_name="Meeting ID",unique=True,blank=True)
        user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,verbose_name="Customer")
        service = models.ForeignKey(Services,on_delete=models.CASCADE,verbose_name="Service",blank=True,null=True)
        expert = models.ForeignKey(Profile,on_delete=models.CASCADE,verbose_name="Expert",blank=True,null=True)
        event = models.ForeignKey(EventScheduleTime,on_delete=models.CASCADE,verbose_name="Meeteing Event",blank=True,null=True)
        join_btn = models.BooleanField(default=False,blank=True,null=True,verbose_name="Join Button")
        add_meeting_btn = models.BooleanField(default=False,blank=True,null=True,verbose_name="Add Meeting Button")
        rating_btn = models.BooleanField(default=False,blank=True,null=True,verbose_name="Rating Button")
        payment_get = models.BooleanField(default=False,blank=True,null=True,verbose_name="Got Meeting Payment")
        refund_enable =  models.BooleanField(default=False,blank=True,null=True,verbose_name="Refund Enable")
        refunded = models.BooleanField(default=False,blank=True,null=True,verbose_name="Meeting Refunded")
        service_name = models.CharField(max_length=100,verbose_name="service_name",blank=True,null=True)
        date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
        rated = models.BooleanField(default=False,blank=True,null=True,verbose_name="Meeting Rated")


        class Meta:
            ordering = ["-date_time"]

        def __str__(self) -> str:
            return self.expert.profile.username+" "+"and"+" "+ self.user.username

class MeetingTypeCount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    meet_45 = models.IntegerField(blank=True,null=True,default=0)
    meet_30 = models.IntegerField(blank=True,null=True,default=0)
    meet_60 = models.IntegerField(blank=True,null=True,default=0)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    date_updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        ordering = ["-date_updated"]

class MeetingRefundContainer(models.Model):
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,null=True,blank=True)
    date_created = models.DateTimeField(auto_created=True,null=True,blank=True)
    def __str__(self) -> str:
        return self.meeting.meeting_id
    class Meta:
        ordering = ["-date_created"]




def pre_save_create_meeting_id(sender, instance, *args, **kwargs):
    if not instance.meeting_id:
        instance.meeting_id= unique_meeting_id_generator(instance)
pre_save.connect(pre_save_create_meeting_id, sender=Meeting)  

