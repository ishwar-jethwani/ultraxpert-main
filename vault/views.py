from rest_framework.permissions import IsAuthenticated
import requests
from requests.auth import HTTPBasicAuth
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID,PAYMANT_BASE_URL
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import *

class CreateCustomer(APIView):
    endpoint = "customers"
    auth=HTTPBasicAuth(username=RAZOR_KEY_ID,password=RAZOR_KEY_SECRET)
    url = PAYMANT_BASE_URL+endpoint
    permission_classes = [IsAuthenticated]
    def post(self,request):
        
        user = Profile.objects.get(profile=request.user)
        try:  
            res = requests.request("GET",url=self.url,auth=self.auth)
            for emails in res.json()["items"]:
                if emails["email"]==user.profile.email:
                    return Response({"res":1,"msg":"you are our old customer",
                                    "data":{"name":str(user.first_name)+str(user.last_name),"email":str(user.profile.email),"contact":str(user.mobile_number)}})
            else:
                payload={
                            "name":str(user.first_name),
                            "email":str(user.profile.email),
                            "contact":str(user.mobile_number),
                            }
                res = requests.request("POST",url=self.url,auth=self.auth,data=payload)

                return Response({"data":res.json()})
        except Exception as e:
                print(e)
                return Response({"res":0,"msg":"somthing went wrong"})
