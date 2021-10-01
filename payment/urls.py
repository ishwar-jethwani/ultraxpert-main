from django.urls import path,include
from .views import *
urlpatterns = [
    path("pay/",PaymentAPIView.as_view(),name="payment")
    
]