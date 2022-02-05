from django.urls import path,include
from .views import *
urlpatterns = [
 
    path("",MeetingAPI.as_view(),name="meet"),
    path("<str:meeting_id>/",get_meet,name="meeting_url"),
    path("expert_meeting/",ExpertMeeting.as_view(),name="expert_meetings")
]