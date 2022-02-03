from django.urls import path
from .views import *

urlpatterns = [
    # path("google_event/<str:service_id>/", GoogleCalaenderAuthorizationAPIView.as_view(), name="google_calander"),
    path("event/", EventCreateAPIView.as_view(), name="event"),
    path("get_event/<service_id>/",GetEventAPIView.as_view(),name="get_event"),
    path("slot/",BookedStatusChangeAPI.as_view(),name="status_changed")

]
