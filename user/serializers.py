from rest_framework import serializers
from .models import *



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment","reply","timestamp"]


class ProfileAutoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name","last_name"]

class ServiceAutoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["service_name","description"] 


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = ["account_holder","bank_name","account_number","ifsc_code"]
    