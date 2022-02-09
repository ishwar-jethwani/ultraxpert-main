from django.urls import path
from .views import *

urlpatterns = [
    path("",CreateVirtualAccount.as_view(),name="create_customer"),
]