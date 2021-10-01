from django.urls import path,include
from .views import *
urlpatterns = [
    path("pay/",ServicePaymentAPIView.as_view(),name="payment")
    
]