from django.urls import path
from .views import *

urlpatterns = [
    path("order_pay/<str:order_id>/",ServicePaymentAPIView.as_view(),name="payment"),
    path("subs_pay/<str:subs_id>/",PlanPaymentAPIView.as_view(),name="subs_payment"),
    path("response/",GetResponse.as_view(),name="response"),
    path("order_create/<str:order_id>/",ServiceOrderCreate.as_view(),name="create_order"),
    path("meeting_order_create/<str:subs_id>/",CreateMeetingOrder.as_view(),name="create_meeting_order"),
    path("pay_link/<str:order_id>/",PaymentLink.as_view(),name="pay_link"),
    path("refund/",RefundAPIView.as_view(),name="refund")  
    
]