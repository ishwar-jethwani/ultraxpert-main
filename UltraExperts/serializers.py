from dataclasses import field
from rest_framework import serializers
from user.models import User

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = ["pk","user_id","is_expert","is_verified","username","email","mobile"]
        model = User

class MobileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["mobile","password"]
        extra_kwargs = {"password":{"write_only":True}}
    def create(self, validated_data):
        password = validated_data.pop("password")
        password1 = self.context["request"].data["password1"]
        if password==password1:
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
            
        
        