from django.urls import path
from .views import *

urlpatterns = [
    path("",CreateCustomer.as_view(),name="create_customer"),
]