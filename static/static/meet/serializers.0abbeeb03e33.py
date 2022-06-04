from UltraExperts.serializers import OrderUserSerilizer, UserSerilizer
from rest_framework.serializers import ModelSerializer
from user.serializers import ProfileSerializer, ServiceShowSerializer
from events.serializers import EventReadSerializer
from rest_framework import serializers

from .models import *
class MeetingSerializer(ModelSerializer):
    user= OrderUserSerilizer()
    service = ServiceShowSerializer()
    expert = ProfileSerializer()
    date_time = serializers.DateTimeField(format="%c")

    class Meta:
        model = Meeting
        fields = "__all__"
        depth = 2

class MeetingContainerSerializer(ModelSerializer):
    user= OrderUserSerilizer()
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = MeetingTypeCount
        fields = "__all__"
