from django.urls import path,include
from .views import *
urlpatterns = [
 
    path("",MeetingAPI.as_view(),name="meet"),
    path("expert_meeting/",ExpertMeeting.as_view(),name="expert_meetings")
]