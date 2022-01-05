from rest_framework.serializers import ModelSerializer
from .models  import *

class SearchSerializer(ModelSerializer):
    class Meta:
        fields = ["query"]
        model = Search