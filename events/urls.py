from django.urls import path
from .views import *

urlpatterns = [
    # path("google_event/<str:service_id>/", GoogleCalaenderAuthorizationAPIView.as_view(), name="google_calander"),
    path("event/", EventCreateAPIView.as_view(), name="event"),

]
