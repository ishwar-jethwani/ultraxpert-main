from rest_framework.serializers import ModelSerializer
from .models import *

class TrainingSerializer(ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"