from rest_framework.permissions import IsAuthenticated
import requests
from requests.auth import HTTPBasicAuth
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID,PAYMANT_BASE_URL
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import *

class CreateVirtualAccount(APIView):
    endpoint2 = "virtual_accounts"
    auth=HTTPBasicAuth(username=RAZOR_KEY_ID,password=RAZOR_KEY_SECRET)
    url = PAYMANT_BASE_URL+endpoint2
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
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
                    "ifsc": "UTIB0000013",
                    "account_number": "914010012345679"
                    }
                }],
                "customer_id":str(user.user_id) ,
        }
        res = requests.request("POST",url=self.url,auth=self.auth,data=payload)
        return Response({"data":res.json()})

