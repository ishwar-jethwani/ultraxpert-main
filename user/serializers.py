from rest_framework import serializers
from .models import *



class KeywordSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = ["id","name"]
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","img"]

class ProfileSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    keywords = KeywordSerilizer()
    class Meta:
        model = Profile
        fields = ["id","first_name","last_name","profile","mobile_number","is_online","title","description","profile_img","gender","country","keywords","categories","user_plan","education","experience"]


class ServicesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    date_created  = serializers.DateTimeField(format="%c")

    class Meta:
        model = Services
        fields = ["service_id","service_img","service_name","category","description","delivery_date","price","currency","tags","date_created"]
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
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = UserPlans
        fields = "__all__"



class CommentSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%c")
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
    