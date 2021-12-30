from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Keywords, User,Profile,Category,SocialMedia,Services, UserPlans
from activity.models import Order
from activity.serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"


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
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlans
        fields = "__all__"
    

class UserPlanSerilizer(serializers.ModelSerializer):
    class Meta:
        model = UserPlans
        fields = "__all__"


class KeywordSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = ["name"]

