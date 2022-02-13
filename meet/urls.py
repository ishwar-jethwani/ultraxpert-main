from django.urls import path,include
from .views import *
urlpatterns = [
 
    path("",MeetingAPI.as_view(),name="meet"),
    path("expert_meeting/",ExpertMeeting.as_view(),name="expert_meetings"),
    path("validation/<str:meeting_id>/",MeetingValidation.as_view(),name="meeting_validation"),
    path("meeting_vault/",MeetingContainer.as_view(),name="meeting_vault")
]