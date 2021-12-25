from django.shortcuts import render
from user.models import *
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from activity.models import Order, Subscriptions
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from UltraExperts.settings import DEBUG
import os
import requests
from requests.auth import HTTPBasicAuth
from activity.models import *

if DEBUG==True:
    BASE_URL = "http://127.0.0.1:8000"
else:
    BASE_URL = os.environ["BASE_URL"]

PAYMANT_BASE_URL = "https://api.razorpay.com/v1/"
# authorize razorpay client with API Keys.


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

                
class ServiceOrderPayment(APIView):
    endpoint = "orders" 
    auth=HTTPBasicAuth(username=RAZOR_KEY_ID,password=RAZOR_KEY_SECRET)
    url = PAYMANT_BASE_URL+endpoint
    permission_classes = [IsAuthenticated]
    def post(self,request,order_id):
        user = Profile.objects.get(profile=request.user)
        try:
            order = Order.objects.get(order_id=order_id)
            payload = {
            "amount": int(order.service_obj.price),
            "currency": order.service_obj.currency,
            "receipt": "Recept"+"-"+order.order_id,
            }
            order_creted = requests.request("POST",url=self.url,auth=self.auth,data=payload)
            if order_creted.json()["status"]=="created":
                self.endpoint = "payment_links"
                self.url = PAYMANT_BASE_URL+self.endpoint
                reference_id = order_creted.json()["id"]
                amount = order_creted.json()["amount"]
                currency = order_creted.json()["currency"]
                payload = {
                    "amount":int(amount*100),
                    "currency": currency,
                    "reference_id": reference_id,
                    "accept_partial": False,
                    "customer": {
                        "name": f"{user.first_name} {user.last_name }",
                        "contact": str(user.mobile_number),
                        "email": str(user.profile.email),
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "reminder_enable": True,
                    "options": {
                            "checkout": {
                            "method": {
                                "netbanking": "1",
                                "card": "1",
                                "upi": "1",
                                "wallet": "1"
                            }
                            }
                        },
                    "notes": {
                        "service_name": f"{order.service_obj.service_name}"
                    },
                    "callback_url": f"{BASE_URL}/{order.order_id}",
                    "callback_method": "get"
                    }

                payload=json.dumps(payload)
                print(payload)
                payment_link = requests.request("POST",url=self.url,auth=self.auth,data=payload)
                return Response((payment_link.json()))

                # self.endpoint = f"payments/{pay_id}/capture"
                # self.url = PAYMANT_BASE_URL+self.endpoint
                # payload = {
                #     "amount":amount,
                #     "currency":currency
                # }
                # payment = requests.request("POST",url=self.url,data=payload,auth=self.auth)
                # return Response(payment.json())
                
        except Exception as e:
            print(e)
            return Response({"res":0,"msg":"somthing went wrong"})


        


        
        
        
                













 
 
# class ServicePaymentAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request,order_id):
#         currency = 'INR'
#         order = Order.objects.get(order_id=order_id)
#         self.amount = int(order.price)*100
#         razorpay_order = razorpay_client.order.create(dict(amount=self.amount,
#                                                         currency=currency,
#                                                         payment_capture='0'))
#         razorpay_order_id = razorpay_order['id']
#         callback_url = '/'
    
#         # we need to pass these details to frontend.
#         context = {}
#         context['razorpay_order_id'] = razorpay_order_id
#         context['razorpay_merchant_key'] = RAZOR_KEY_ID
#         context['razorpay_amount'] = self.amount
#         context['currency'] = currency
#         context['callback_url'] = callback_url
#         return render(request,"payment.html",context)

#     @csrf_exempt
#     def post(self,request):
#         payment_id = request.POST.get('razorpay_payment_id', '')
#         razorpay_order_id = request.POST.get('razorpay_order_id', '')
#         signature = request.POST.get('razorpay_signature', '')
#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         }
#         razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#         capture = razorpay_client.payment.capture(payment_id, self.amount)
#         if capture:
#             return render(request, 'paymentsuccess.html')
#         else:
#             return render(request, 'paymentfail.html')


# class PlanPaymentAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request,subs_id):
#         print(Authorization)
#         currency = 'INR'
#         subscibers = Subscriptions.objects.get(subs_id=subs_id)
#         self.amount = int(subscibers.plan.plan_price)*100
#         razorpay_order = razorpay_client.order.create(dict(amount=self.amount,
#                                                         currency=currency,
#                                                         payment_capture='0'))
#         razorpay_order_id = razorpay_order['id']
#         callback_url = '/'
    
#         # we need to pass these details to frontend.
#         context = {}
#         context['razorpay_order_id'] = razorpay_order_id
#         context['razorpay_merchant_key'] = RAZOR_KEY_ID
#         context['razorpay_amount'] = self.amount
#         context['currency'] = currency
#         context['callback_url'] = callback_url
#         return render(request,"payment.html",context)

#     @csrf_exempt
#     def post(self,request):
#         payment_id = request.POST.get('razorpay_payment_id', '')
#         razorpay_order_id = request.POST.get('razorpay_order_id', '')
#         signature = request.POST.get('razorpay_signature', '')
#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         }

#         razorpay_client.utility.verify_payment_signature(params_dict)

#         amount = self.amount 
#         capture = razorpay_client.payment.capture(payment_id, amount)
 
#         if capture:         # render success page on successful caputre of payment
#             return render(request, 'paymentsuccess.html')
#         else:
#             return render(request, 'paymentfail.html')
  

# class GetResponse(APIView):
#     def post(self,request):
#         data = request.data
#         order_id = data["payload"]["payment"]["entity"]["order_id"]
#         print("response",data)
#         payment_data = PaymentStatus.objects.create(order_no=order_id,response=data)
#         if payment_data:
#             payment_created = PaymantStatusSerializer(payment_data)
#             return Response(data=payment_created.data)

#     def get(self,request):
#         order_no = request.data["payload"]["payment"]["entity"]["order_id"]
#         data = PaymentStatus.objects.get(order_no=order_no)
#         payment_created = PaymantStatusSerializer(data)
#         return Response(data = payment_created.data) 


