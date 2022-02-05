from UltraExperts.serializers import UserSerilizer
from rest_framework.serializers import ModelSerializer
from user.serializers import ProfileSerializer, ServiceShowSerializer
from events.serializers import EventReadSerializer
from rest_framework import serializers

from .models import *
class MeetingSerializer(ModelSerializer):
    user= UserSerilizer()
    service = ServiceShowSerializer()
    event = EventReadSerializer()
    expert = ProfileSerializer()
    date_time = serializers.DateTimeField(format="%c")

    class Meta:
        model = Meeting
        fields = "__all__"
        depth = 2