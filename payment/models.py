from django.db import models
#Payment Status Model
class PaymentStatus(models.Model):
    """Model For Payment Status"""
    payment_id = models.CharField(max_length=20,verbose_name="payment_id",blank=True)
    order_no = models.CharField(max_length=20,verbose_name="order_no",blank=True,null=True)
    response = models.JSONField(verbose_name="response",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status = models.CharField(max_length=50,verbose_name="status",blank=True,null=True)

    def __str__(self) -> str:
        return self.order_no

    class Meta:
        ordering = ["-date_created"]

#Refund Status Model
class RefundStatus(models.Model):
    """Model For Refund Status"""
    refund_id = models.CharField(max_length=500,verbose_name="Refund ID",blank=True,null=True)
    response = models.JSONField(verbose_name="Refund Response",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.refund_id

    class Meta:
        ordering = ["-date_created"]




