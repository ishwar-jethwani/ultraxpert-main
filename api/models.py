from user.models import Services, User, User_Plans
from django.db import models
from .utils import * 
from django.db.models.signals import pre_save





class Event(models.Model):

    notify_choices = (
    ('5 Minutes',5),
    ('10 Minutes',10),
    ('15 Minutes',15),
    ('30 Minutes',30),
    ('1 Hour',60),

)

    event_id = models.CharField(max_length=20,verbose_name="Event ID",unique=True,blank=True)
    event_name = models.CharField(max_length=100,verbose_name="Event Name",blank=True)
    discription = models.CharField(max_length=500,verbose_name="Discription",blank=True)
    expert = models.ForeignKey(User,on_delete=models.CASCADE)
    releted_service = models.ForeignKey(Services,on_delete=models.CASCADE,null=True)
    notify_before = models.BooleanField(default=False)
    notify_before_time = models.CharField(max_length=50,choices=notify_choices,verbose_name="Notify Before Time",blank=True,null=True)
    notify_after = models.BooleanField(default=False)
    notify_after_time = models.CharField(max_length=50,choices=notify_choices,verbose_name="Notify After Time",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_id
    
    class Meta:
        ordering = ["-date_updated"]

    @property
    def schedules(self):
        return self.eventschedule_set.all()


class EventSchedule(models.Model):
    day = models.CharField(verbose_name="Day",max_length=30)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return "{}-{}".format(str(self.id), str(self.event.event_id))

    @property
    def timings(self):
        return self.eventscheduletime_set.all()

class EventScheduleTime(models.Model):
    start_time  = models.CharField(max_length=255,verbose_name="start time",blank=True,null=True)
    end_time    = models.CharField(max_length=255,verbose_name="start time",blank=True,null=True)
    timezone    = models.CharField(max_length=255,verbose_name="timeZone",default="Asia/Kuwait")
    schedule    = models.ForeignKey(EventSchedule,models.CASCADE)

    def __str__(self) -> str:
        return "{}-{}-{}".format(str(self.id), str(self.schedule.id),str(self.schedule.event.event_id))

class PaymentStatus(models.Model):
    payment_id = models.CharField(max_length=20,verbose_name="payment_id",blank=True)
    order_no = models.CharField(max_length=20,verbose_name="order_no")
    response = models.JSONField(verbose_name="response")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.order_no

    class Meta:
        ordering = ["-date_created"]






def pre_save_create_event_id(sender, instance, *args, **kwargs):
    if not instance.event_id:
        instance.event_id= unique_event_id_generator(instance)


pre_save.connect(pre_save_create_event_id, sender=Event)




def pre_save_create_payment_id(sender, instance, *args, **kwargs):
    if not instance.payment_id:
        instance.payment_id= unique_payment_id_generator(instance)


pre_save.connect(pre_save_create_payment_id, sender=PaymentStatus)


