from events.models import Event
from django.urls import path,include
from .views import *
from agora.views import Agora
from .constant import AGORA_APP_ID, CHANNEL
urlpatterns = [
    path("google_event/<str:service_id>/", GoogleCalaenderAuthorizationAPIView.as_view(), name="google_calander"),
    path("event/", EventCreateAPIView.as_view(), name="event"),

]
