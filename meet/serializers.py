from UltraExperts.serializers import OrderUserSerilizer, UserSerilizer
from rest_framework.serializers import ModelSerializer
from user.serializers import ProfileSerializer, ServiceShowSerializer
from events.serializers import EventReadSerializer
from rest_framework import serializers
from .models import *

#Meeting Serilizer
class MeetingSerializer(ModelSerializer):
    """ModelSerializer For Meeting"""
    user= OrderUserSerilizer()
    service = ServiceShowSerializer()
    expert = ProfileSerializer()
    date_time = serializers.DateTimeField(format="%c")

    class Meta:
        model = Meeting
        fields = "__all__"
        depth = 2

#Meeting Container Serilizer
class MeetingContainerSerializer(ModelSerializer):
    """ModelSerializer For Meeting Container"""
    user= OrderUserSerilizer()
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = MeetingTypeCount
        fields = "__all__"
