from django.urls import path,include
from .views import *
urlpatterns = [
    path("<str:meeting_id>/",MeetingAPI.as_view(),name="meet")
]