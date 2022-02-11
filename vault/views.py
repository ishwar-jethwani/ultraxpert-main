from rest_framework.permissions import IsAuthenticated
import requests
from requests.auth import HTTPBasicAuth
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID,PAYMANT_BASE_URL
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import *
import razorpay
from rest_framework import status


# client.virtual_account.create(data=DATA)
# DATA should contain these keys
#     receiver_types        : ['bank_account']
#     description           : 'Random Description'
#     customer_id(optional) : <CUSTOMER_ID>

class CreateVirtualAccount(APIView):
    client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        bank_account = BankDetail.objects.filter(user=user).first()
        payload = {
                "receivers": {
                    "types": [
                        "bank_account"
                    ]
                },
                "allowed_payers": 
                [{
                    "type": "bank_account",
                    "bank_account": {
                    "ifsc": f"{bank_account.ifsc_code}",
                    "account_number": f"{bank_account.account_number}"
                    }
                }],
                "customer_id":str(user.user_id) ,
        }
        res = self.client.virtual_account.create(data=payload)
        return Response({"data":res.json()},status=status.HTTP_201_CREATED)

