from rest_framework.serializers import ModelSerializer
from .models  import *
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *

class ExpertDocumentSerializer(DocumentSerializer):
    class Meta:
        fields = ["first_name","last_name","title","description"]
        document=ExpertsDocument


class SearchSerializer(ModelSerializer):
    class Meta:
        fields = ["query"]
        model = Search