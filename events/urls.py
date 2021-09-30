from events.models import Event
from django.urls import path,include
from .views import *
from agora.views import Agora
from .constant import AGORA_APP_ID, CHANNEL
urlpatterns = [
    path("google_event/<str:service_id>/", GoogleCalaenderAuthorizationAPIView.as_view(), name="google_calander"),
    path("event/", EventCreateAPIView.as_view(), name="event"),
    path("payement_response/", GetResponse.as_view(), name="response"),
    path("payement_subs_response/", GetSubsResponse.as_view(), name="response_subs"),
    path("payment/<str:order_id>/", PaymentAPIView.as_view(), name="payment"),
    path('agora/', Agora.as_view(app_id=AGORA_APP_ID, channel=CHANNEL))

]
