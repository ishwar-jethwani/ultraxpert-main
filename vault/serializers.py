from pyexpat import model
from rest_framework.serializers import ModelSerializer
from .models import *

class RazorPayCustomerSerializer(ModelSerializer):
   class Meta:
       fields = ["cust_id","cust_name","cust_email"]
       model = RazorPayCustomer
    
class RazorPayVirtualAccountSerializer(ModelSerializer):
   class Meta:
       fields = ["cust_id","virual_account_id","virual_data"]
       model = VirtualAccount