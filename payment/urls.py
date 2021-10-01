from django.urls import path,include
from .views import *
urlpatterns = [
    path("pay/<str:order_id>/",ServicePaymentAPIView.as_view(),name="payment"),
    path("subs_pay/<str:subs_id>/",PlanPaymentAPIView.as_view(),name="subs_payment")
    
]