from rest_framework import serializers
from user.models import User

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = ["pk","user_id","is_expert","is_verified","username","email","mobile"]
        model = User