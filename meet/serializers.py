from UltraExperts.serializers import UserSerilizer
from rest_framework.serializers import ModelSerializer
from user.serializers import ServiceShowSerializer
from events.serializers import EventReadSerializer

from .models import *
class MeetingSerializer(ModelSerializer):
    user= UserSerilizer()
    service = ServiceShowSerializer()
    event = EventReadSerializer()

    class Meta:
        model = Meeting
        fields = "__all__"
        depth = 2