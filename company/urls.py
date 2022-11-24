from django.urls import path
from .views import *

urlpatterns = [
    path("training/",TriningList.as_view(),name="training"),
]