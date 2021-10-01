from django.db import models
from .utils import *
from django.db.models.signals import pre_save



class PaymentStatus(models.Model):
    payment_id = models.CharField(max_length=20,verbose_name="payment_id",blank=True)
    order_no = models.CharField(max_length=20,verbose_name="order_no")
    response = models.JSONField(verbose_name="response")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.order_no

    class Meta:
        ordering = ["-date_created"]


def pre_save_create_payment_id(sender, instance, *args, **kwargs):
    if not instance.payment_id:
        instance.payment_id= unique_payment_id_generator(instance)


pre_save.connect(pre_save_create_payment_id, sender=PaymentStatus)
