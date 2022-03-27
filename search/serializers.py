from rest_framework.serializers import ModelSerializer
from .models  import *
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *
from UltraExperts.serializers import UserSerilizer

class ExpertDocumentSerializer(DocumentSerializer):
    class Meta:
        fields = [
            "first_name",
            "last_name",
            "profile",
            "profile_img",
            "gender",
            "is_online",
            "title",
            "education",
            "experience",
            "country"
        ]
        document=ExpertsDocument
        depth = 1
class ServiceDocumentSerializer(DocumentSerializer):
    class Meta:
        fields = [
            "service_id",
            "service_name",
            "service_img",
            "category",
            "price",
            "tags",
            "title"
        ]
        document=ServiceDocument

class SearchSerializer(ModelSerializer):
    class Meta:
        fields = ["query"]
        model = Search



class ExpertSearchSerializer(ModelSerializer):
    class Meta:
        fields = [
            "first_name",
            "last_name",
            "profile",
            "profile_img",
            "gender",
            "is_online",
            "title",
            "education",
            "experience",
            "country"
        ]
        model= Profile
        depth = 1
class ServiceSearchSerializer(ModelSerializer):
    class Meta:
        fields = [
            "service_id",
            "service_name",
            "service_img",
            "category",
            "price",
            "tags"
        ]
        model=Services
        