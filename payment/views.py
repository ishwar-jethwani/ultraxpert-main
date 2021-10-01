from django.shortcuts import render
from django.views.generic.base import RedirectView
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from activity.models import Order, Subscriptions
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from user.models import Services

 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
 
 
class ServicePaymentAPIView(APIView):
    def get(self,request,order_id):
        currency = 'INR'
        order = Order.objects.get(order_id=order_id)
        amount = int(order.price)*100
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = 'pay/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request,"payment.html")

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

        result = razorpay_client.utility.verify_payment_signature(
                params_dict)
        if result is None:
            amount = 20000  # Rs. 200
            try:
                razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                return render(request, 'paymentsuccess.html')
            except:
                    # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
        else:
            return render(request, 'paymentfail.html')

class PlanPaymentAPIView(APIView):
    def get(self,request,subs_id):
        currency = 'INR'
        subscibers = Subscriptions.objects.get(subs_id=subs_id)
        amount = int(subscibers.plan.plan_price)*100
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = 'pay/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request,"payment.html")

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

        result = razorpay_client.utility.verify_payment_signature(
                params_dict)
        if result is None:
            amount = 20000  # Rs. 200
            try:
                razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                return render(request, 'paymentsuccess.html')
            except:
                    # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
        else:
            return render(request, 'paymentfail.html')    

