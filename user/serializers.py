from rest_framework import serializers
from .models import *
from UltraExperts.serializers import *

class KeywordSerilizer(serializers.ModelSerializer):
    """ModelSerializer For Model Keyword"""
    class Meta:
        model = Keywords
        fields = ["id","name"]
class CategorySerializer(serializers.ModelSerializer):
    """ModelSerializer For Model Category"""
    class Meta:
        model = Category
        fields = ["id","name","img"]

class ProfileSerializer(serializers.ModelSerializer):
    """ModelSerializer For Model Profile"""
    categories = CategorySerializer()
    keywords = KeywordSerilizer()
    profile = OrderUserSerilizer()
    class Meta:
        model = Profile
        fields = ["id","first_name","last_name","profile","mobile_number","is_online","title","description","profile_img","gender","country","keywords","categories","user_plan","education","experience"]


class ServiceShowSerializer(serializers.ModelSerializer):
    """ModelSerializer For Displaying Service"""
    category = CategorySerializer()
    date_created  = serializers.DateTimeField(format="%c")
    user = OrderUserSerilizer()
    class Meta:
        model = Services
        fields = ["user","id","service_id","service_img","service_name","category","description","delivery_date","price","currency","tags","date_created"]


class ServicesSerializer(serializers.ModelSerializer):
    """ModelSerializer For Model Service"""
    class Meta:
        model = Services
        fields = "__all__"
        read_only = ["user"]

    def __init__(self, *args, **kwargs):
        super(ServicesSerializer, self).__init__(*args, **kwargs)

        if 'context' in kwargs:
            if 'request' in kwargs['context']:
                tabs = kwargs['context']['request'].query_params.getlist('tab', [])
                if tabs:
                    included = set(tabs)
                    existing = set(self.fields.keys())

                    for other in existing - included:
                        self.fields.pop(other)

    def create(self, validated_data):
        validated_data.pop("user")
        user = self.context["request"].user
        if user.is_expert == True:
            service = Services.objects.create(**validated_data, user=user)
            return service
    

class UserPlanSerilizer(serializers.ModelSerializer):
    """ModelSerializer For Model User Plan"""
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = UserPlans
        fields = "__all__"



class CommentSerializer(serializers.ModelSerializer):
    """ModelSerializer For Model Comment"""
    timestamp = serializers.DateTimeField(format="%c")
    class Meta:
        model = Comment
        fields = "__all__"


class ProfileAutoCompleteSerializer(serializers.ModelSerializer):
    """ModelSerializer For Auto Completing User Profiles"""
    def to_representation(self, instance):
        return {
            "name":f"{instance.first_name} {instance.last_name}",
            "description":instance.description
        }
    class Meta:
        model = Profile
        fields = ["first_name","last_name"]

class ServiceAutoCompleteSerializer(serializers.ModelSerializer):
    """ModelSerializer For Auto Completing Services"""
    def to_representation(self, instance):
        return {
            "name":instance.service_name,
            "description":instance.description
        }
    class Meta:
        model = Services

class BankSerializer(serializers.ModelSerializer):
    """ModelSerializer For Model Bank"""
    class Meta:
        model = BankDetail
        fields = ["user","account_holder","bank_name","account_number","ifsc_code"]
        def create(self, validated_data):
            validated_data.pop("user")
            user = self.context["request"].user
            if user.is_expert == True:
                service = BankDetail.objects.create(**validated_data, user=user)
                return service

class TestSerializer(serializers.ModelSerializer):
    """ModelSerializer For Model Test"""
    class Meta:
        model = Test
        fields = "__all__"

class UserTestReportSerializer(serializers.ModelSerializer):
    """Serilizer For User Report"""
    class Meta:
        model = UserTestReport
        fields = "__all__"