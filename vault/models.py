from statistics import mode
from django.db import models

# Create your models here.
class RazorPayCustomer(models.Model):
    cust_id = models.CharField(max_length=50,verbose_name="CustomerID",blank=True,null=True)
    cust_name = models.CharField(max_length=50,verbose_name="CustomerName",blank=True,null=True)
    cust_email = models.CharField(max_length=50,verbose_name="CustomerEmail",blank=True,null=True)
    date_created = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.cust_id
    
    class Meta:
        ordering=["-date_created"]

class VirtualAccount(models.Model):
    cust_id = models.CharField(max_length=50,verbose_name="CustomerID",blank=True,null=True)
    virual_account_id = models.CharField(max_length=50,verbose_name="Virtual Account ID",blank=True,null=True)
    virual_data = models.JSONField(blank=True,null=True)
    def __str__(self) -> str:
        return self.virual_account_id