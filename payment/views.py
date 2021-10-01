from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from activity.models import Order, Subscriptions
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
 
 
class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        currency = 'INR'
        type = request.data["type"]
        if type == "Plan":
            sub_id = request.data["subs_id"]
            subscription = Subscriptions.objects.get(subs_id=sub_id)
            amount = int(subscription.plan.plan_price)*100
        else:
            order_id = request.data["order_id"]
            order = Order.objects.get(order_id=order_id)
            amount = int(order.price)*100


    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'pay/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return Response(context,status=HTTP_201_CREATED)

    @csrf_exempt
    def post(self,request):

        try:
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
                    return Response({
                            "order_id":params_dict[razorpay_order_id],
                            "payment_id":params_dict["razorpay_payment_id"],
                            "status":"sucess"
                        })
                except:
                    return Response({
                            "order_id":params_dict[razorpay_order_id],
                            "payment_id":params_dict["razorpay_payment_id"],
                            "status":"failed"
                        })
            else:
                return Response({
                        "order_id":params_dict[razorpay_order_id],
                        "payment_id":params_dict["razorpay_payment_id"],
                        "status":"signature failed"
                    })
        except:
            return HttpResponseBadRequest()
