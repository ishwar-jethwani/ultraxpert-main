from os import name
from django.urls import path,include
from .views import *
urlpatterns = [
    # path("pay/<str:order_id>/",ServicePaymentAPIView.as_view(),name="payment"),
    # path("subs_pay/<str:subs_id>/",PlanPaymentAPIView.as_view(),name="subs_payment"),
    # path("response/",GetResponse.as_view(),name="response")
    path("create_customer/",CreateCustomer.as_view(),name="create_customer"),
    path("pay/<str:order_id>/",ServiceOrderPayment.as_view(),name="pay_order")
    
]