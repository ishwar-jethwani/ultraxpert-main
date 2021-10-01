from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from UltraExperts.constants import RAZOR_KEY_SECRET,RAZOR_KEY_ID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from activity.models import Order
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
 
 
class PaymentAPIView(APIView):
    def get(self,request):
        currency = 'INR'
        order_id = request.data["order_id"]
        order = Order.objects.get(order_id=order_id)
        amount = order.price
    
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
        if request.method == "POST":
            try:
            
                # get the required parameters from post request.
                payment_id = request.POST.get('razorpay_payment_id', '')
                razorpay_order_id = request.POST.get('razorpay_order_id', '')
                signature = request.POST.get('razorpay_signature', '')
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
    
                # verify the payment signature.
                result = razorpay_client.utility.verify_payment_signature(
                    params_dict)
                if result is None:
                    amount = 20000  # Rs. 200
                    try:
    
                        # capture the payemt
                        razorpay_client.payment.capture(payment_id, amount)
    
                        # render success page on successful caputre of payment
                        return Response({
                                "order_id":params_dict[razorpay_order_id],
                                "payment_id":params_dict["razorpay_payment_id"],
                                "status":"sucess"
                            })
                    except:
    
                        # if there is an error while capturing payment.
                        return Response({
                                "order_id":params_dict[razorpay_order_id],
                                "payment_id":params_dict["razorpay_payment_id"],
                                "status":"failed"
                            })
                else:
    
                    # if signature verification fails.
                     return Response({
                                "order_id":params_dict[razorpay_order_id],
                                "payment_id":params_dict["razorpay_payment_id"],
                                "status":"signature failed"
                            })
            except:
    
                # if we don't find the required parameters in POST data
                return HttpResponseBadRequest()
        else:
        # if other than POST request is made.
            return HttpResponseBadRequest()
