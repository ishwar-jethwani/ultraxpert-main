from django.urls import path,include
from .views import *
urlpatterns = [
    path("",MeetingAPI.as_view(),name="meet")
]