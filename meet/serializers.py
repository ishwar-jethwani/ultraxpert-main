from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import *
class MeetingSerializer(ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        depth = 1