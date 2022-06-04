from rest_framework import serializers
from user.models import User
from .models import *

# class MessageSerializer(serializers.ModelSerializer):
#     sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
#     receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
#     class Meta:
#         model = Message
#         fields = ['sender', 'receiver', 'message', 'timestamp']