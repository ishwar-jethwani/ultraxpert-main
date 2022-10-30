from dataclasses import field
from statistics import mode
from rest_framework import serializers
from .models import *
from UltraExperts.serializers import *

#Serilizer For Keyword

class KeywordSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = ["id","name"]

#Serilizer For Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","img"]

#Serilizer For Profile

class ProfileSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    keywords = KeywordSerilizer()
    profile = OrderUserSerilizer()
    class Meta:
        model = Profile
        fields = ["id","first_name","last_name","profile","mobile_number","is_online","title","description","profile_img","gender","country","keywords","categories","user_plan","education","experience"]


#Serilizer For Showing Service

class ServiceShowSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    date_created  = serializers.DateTimeField(format="%c")
    user = OrderUserSerilizer()
    class Meta:
        model = Services
        fields = ["user","id","service_id","service_img","service_name","category","description","delivery_date","price","currency","tags","date_created"]

#Serilizer For Service

class ServicesSerializer(serializers.ModelSerializer):
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

#Serilizer For User Plan

class UserPlanSerilizer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = UserPlans
        fields = "__all__"


#Serilizer For Comment

class CommentSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%c")
    class Meta:
        model = Comment
        fields = "__all__"

#Serilizer For Autocompleting Profile

class ProfileAutoCompleteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            "name":f"{instance.first_name} {instance.last_name}",
            "description":instance.description
        }
    class Meta:
        model = Profile
        fields = ["first_name","last_name"]

#Serilizer For Autocompleting Service

class ServiceAutoCompleteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            "name":instance.service_name,
            "description":instance.description
        }
    class Meta:
        model = Services

#Serilizer For Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = ["user","account_holder","bank_name","account_number","ifsc_code"]
        def create(self, validated_data):
            validated_data.pop("user")
            user = self.context["request"].user
            if user.is_expert == True:
                service = BankDetail.objects.create(**validated_data, user=user)
                return service
    