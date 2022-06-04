from django.urls import path
from .views import *

urlpatterns = [
    path("",CreateVirtualAccount.as_view(),name="create_customer"),
    path("transfer/<str:pay_id>/",TransferApi.as_view(),name="transfer")
]