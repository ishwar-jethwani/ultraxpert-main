from rest_framework.permissions import IsAuthenticated
import requests
from requests.auth import HTTPBasicAuth
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID,PAYMANT_BASE_URL
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import *
import razorpay
from rest_framework import status
from .models import *
from .serializers import *


# client.virtual_account.create(data=DATA)
# DATA should contain these keys
#     receiver_types        : ['bank_account']
#     description           : 'Random Description'
#     customer_id(optional) : <CUSTOMER_ID>




def create_customer(user):
    endpoint = "customers"
    auth=HTTPBasicAuth(username=RAZOR_KEY_ID,password=RAZOR_KEY_SECRET)
    url = PAYMANT_BASE_URL+endpoint
    user = Profile.objects.get(profile=user)
    res = requests.request("GET",url=url,auth=auth)
    email_list = []
    if len(res.json()["items"])>0:
        for emails in res.json()["items"]:
            email_list.append(emails["email"])
        if user.profile.email in email_list:
            data=RazorPayCustomer.objects.get(cust_email=emails["email"])
            serialize = RazorPayCustomerSerializer(data)
            return serialize.data
        else:           
            payload={
                    "name":str(user.first_name),
                    "email":str(user.profile.email),
                    }
            res = requests.request("POST",url=url,auth=auth,data=payload)
            if res.json()["id"]:
                data = RazorPayCustomer.objects.create(cust_id=res.json()["id"],cust_name=res.json()["name"],cust_email=res.json()["email"])
                serialize = RazorPayCustomerSerializer(data)
                return serialize.data
    else:           
        payload={
                "name":str(user.first_name),
                "email":str(user.profile.email),
                }
        res = requests.request("POST",url=url,auth=auth,data=payload)
        if res.json()["id"]:
            data = RazorPayCustomer.objects.create(cust_id=res.json()["id"],cust_name=res.json()["name"],cust_email=res.json()["email"])
            serialize = RazorPayCustomerSerializer(data)
            return serialize.data


class CreateVirtualAccount(APIView):
    client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        customer_id = create_customer(user)
        customer_id = customer_id["cust_id"]
        virtual_account = VirtualAccount.objects.filter(cust_id=customer_id)
        if virtual_account.exists():
            virtual_account_id = virtual_account.first().virual_account_id
            res =self.client.virtual_account.fetch(virtual_account_id=virtual_account_id)
            return Response(res,status=status.HTTP_200_OK)
        else:
            return Response({"msg":"You Dont have virtual account"},status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):
        user = request.user
        customer_id = create_customer(user)
        customer_id = customer_id["cust_id"]
        virtual_account = VirtualAccount.objects.filter(cust_id=customer_id)
        if virtual_account.exists():
            serialize = RazorPayVirtualAccountSerializer(virtual_account,many=True)
            return Response(serialize.data,status=status.HTTP_200_OK)
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
                "customer_id":customer_id ,
        }
        print(payload)
        res = self.client.virtual_account.create(data=payload)
        print(res)
        if res:
            virtual_account_create = VirtualAccount.objects.create(cust_id=customer_id,virual_account_id=res["id"],virual_data=res)
            if virtual_account_create:
                serialize = RazorPayVirtualAccountSerializer(virtual_account_create)
                return Response(serialize.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"msg":"Somthing Went Wrong"},status=status.HTTP_400_BAD_REQUEST)

