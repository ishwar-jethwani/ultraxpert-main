from django.shortcuts import render
from user.models import *
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID,PAYMANT_BASE_URL
from UltraExperts.settings import BASE_URL
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from activity.models import Order, Subscriptions
from rest_framework.permissions import IsAuthenticated
import requests
from requests.auth import HTTPBasicAuth
from activity.models import *
import razorpay
import json
from datetime import datetime,timedelta
from django.core.mail import send_mail
from django.template.loader import get_template
# authorize razorpay client with API Keys.


razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

#View For Create Service  
               
class ServiceOrderCreate(APIView):
    """Service Creation"""
    endpoint = "orders" 
    auth=HTTPBasicAuth(username=RAZOR_KEY_ID,password=RAZOR_KEY_SECRET)
    url = PAYMANT_BASE_URL+endpoint
    permission_classes = [IsAuthenticated]
    def post(self,request,order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            payload = {
            "amount": int(order.service_obj.price)*100,
            "currency": order.service_obj.currency,
            "receipt": "Recept"+"-"+order.order_id,
            }
            order_creted = requests.request("POST",url=self.url,auth=self.auth,data=payload)
            return Response(order_creted.json()) 
        except Exception as e:
            print(e)
            return Response({"res":0,"msg":"somthing went wrong"})

#View For Create Meeting

class CreateMeetingOrder(APIView):
    """Meeting Order Generation"""
    endpoint = "orders" 
    auth=HTTPBasicAuth(username=RAZOR_KEY_ID,password=RAZOR_KEY_SECRET)
    url = PAYMANT_BASE_URL+endpoint
    permission_classes = [IsAuthenticated]
    def post(self,request,subs_id):
        meetings = int(request.data["meetings"])
        try:
            meeting_order = Subscriptions.objects.get(subs_id=subs_id)
            payload = {
            "amount": int(meeting_order.plan.plan_price)*100*meetings,
            "currency": meeting_order.plan.currency,
            "receipt": "Recept"+"-"+meeting_order.subs_id,
            }
            order_creted = requests.request("POST",url=self.url,auth=self.auth,data=payload)
            return Response(order_creted.json())
                
        except Exception as e:
            print(e)
            return Response({"res":0,"msg":"somthing went wrong"})

#View For Making Payments

class PaymentLink(APIView):
    """Payment Link Activation"""
    endpoint = "payment_links"
    auth=HTTPBasicAuth(username=RAZOR_KEY_ID,password=RAZOR_KEY_SECRET)
    url = PAYMANT_BASE_URL+endpoint
    permission_classes = [IsAuthenticated]
    def get(self,request, order_id):
        user = Profile.objects.get(profile=request.user)
        try:
            order = Order.objects.get(order_id=order_id)
            reference_id = order.order_id
            amount = order.service_obj.price
            currency = order.service_obj.currency
            payload = {
                    "amount":20000,# this is a integer value
                    "currency": str(currency),
                    "reference_id":"new_123456",
                    # "description": f"Pay for {order.service_obj.service_name} ",
                    "customer": {
                        "name": f"{user.first_name} {user.last_name }",
                        "contact": str(user.mobile_number),
                        "email": str(user.profile.email),
                    },
                    # "notes": {
                    #     "service_name": f"{order.service_obj.service_name}"
                    # },
                    "callback_url": f"{BASE_URL}",
                    "callback_method": "get"
                    }

            print(payload)
            print(self.url)
            print(type(payload["amount"]))
            payment_link = requests.request("POST",url=self.url,auth=self.auth,data=payload)
            return Response(payment_link.json())


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



# Payment BY default checkout

class ServicePaymentAPIView(APIView):
    """"Payment OF Service By Default Checkout"""
    permission_classes = [IsAuthenticated]
    def get(self,request,order_id):
        currency = 'INR'
        order = Order.objects.get(order_id=order_id)
        self.amount = int(order.price)*100
        razorpay_order = razorpay_client.order.create(dict(amount=self.amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = '/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = self.amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request,"payment.html",context)

    @csrf_exempt
    def post(self,request):
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        razorpay_client.utility.verify_payment_signature(
                params_dict)
        capture = razorpay_client.payment.capture(payment_id, self.amount)
        if capture:
            return render(request, 'paymentsuccess.html')
        else:
            return render(request, 'paymentfail.html')

# View For Making Payments According To Plan

class PlanPaymentAPIView(APIView):
    """"Payment According To Plan """
    permission_classes = [IsAuthenticated]
    def get(self,request,subs_id):
        currency = 'INR'
        subscibers = Subscriptions.objects.get(subs_id=subs_id)
        self.amount = int(subscibers.plan.plan_price)*100
        razorpay_order = razorpay_client.order.create(dict(amount=self.amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = '/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = self.amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request,"payment.html",context)

    @csrf_exempt
    def post(self,request):
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        razorpay_client.utility.verify_payment_signature(params_dict)

        amount = self.amount 
        capture = razorpay_client.payment.capture(payment_id, amount)
 
        if capture:         # render success page on successful caputre of payment
            return render(request, 'paymentsuccess.html')
        else:
            return render(request, 'paymentfail.html')


# View For Checking Payment Staus 

class GetResponse(APIView):
    """Checking Of Status Of Payment"""
    def post(self,request):
        data = request.data
        payment_id = data["payload"]["payment"]["entity"]["id"]
        order_id = data["payload"]["payment"]["entity"]["order_id"]
        status = data["payload"]["payment"]["entity"]["status"]
        payment_data = PaymentStatus.objects.create(payment_id=payment_id,order_no=order_id,response=data,status=status)
        if payment_data:
            payment_created = PaymantStatusSerializer(payment_data)
            return Response(data=payment_created.data,status=HTTP_201_CREATED)

    def get(self,request):
        order_no = request.data["payload"]["payment"]["entity"]["order_id"]
        data = PaymentStatus.objects.get(order_no=order_no)
        payment_created = PaymantStatusSerializer(data)
        return Response(data = payment_created.data,status=HTTP_200_OK) 


# View For Making Payment REfund

class RefundAPIView(APIView):
    """"Refund Of Payment"""
    permission_classes = [IsAuthenticated]
    def post(self,request,order_id):
        reason_value = request.GET["reason"]
        type = request.GET["type"]
        reason = {"reason":reason_value}
        order = Order.objects.filter(order_id=order_id)
        current_time = datetime.now()
        if order.exists():
            start_time = order.first().slot.start_time
            date  = order.first().slot.schedule.day
            start_meeting_start_time = datetime.strptime(date+"/"+start_time,"%d/%m/%Y/%H:%M")
            if current_time>=start_meeting_start_time+timedelta(hours=6):
                if order.first().paid == True and order.first().status=="booked":
                    payment = PaymentStatus.objects.get(order_no=order.first().order_no)
                    razorpay_payment_id = payment.response["payload"]["payment"]["entity"]["id"]
                    amount_payment_amount = ((payment.response["payload"]["payment"]["entity"]["amount"])/100)*50/100
                    if type == "instant":
                        speed = "optimum"
                        refund = razorpay_client.payment.refund(razorpay_payment_id, amount_payment_amount,notes=reason,speed=speed)
                    else:
                        refund = razorpay_client.payment.refund(razorpay_payment_id, amount_payment_amount,notes=reason,speed=type)
                    if refund:
                        refund_id = refund["id"]
                        save_refund = RefundStatus(refund_id=refund_id,response=refund).save()
                        if save_refund:
                            order.update(status="cancelled")
                            return Response({"msg":"amount is refunded sucessfully","data":refund},status=HTTP_200_OK)
        else:
            return Response({"msg":"amount is not refunded sucessfully","data":refund})



#View For Creating Invoice

class InvoiceAPIView(APIView):
    """Generating Invoice"""
    def post(self,request):
        data = request.data
        invoice = razorpay_client.invoice.create(data=data)
        return Response(invoice,status=HTTP_200_OK)





# payment_id = "<PAYMENT_ID>"

# payment_amount = "<payment_amount>"

# resp = razorpay_client.payment.refund(payment_id, payment_amount)

# #Refund with Extra Parameters

# notes = {'key': 'value'}

# resp = razorpay_client.payment.refund(payment_id, payment_amount, notes=notes)