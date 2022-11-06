from rest_framework import serializers
from .models import *

class AboutUsSerializer(serializers.ModelSerializer):
    """ModelSerializer For About US Model"""
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = AboutUs
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    """ModelSerializer For Banner Model """
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = Banner
        fields = "__all__"

class SupportQuerySerializer(serializers.ModelSerializer):
    """ModelSerializer Support Query Model"""
    class Meta:
        model = SupportQuery
        fields = ["name","contact_number","email","subject","message"]


class BlogSerializer(serializers.ModelSerializer):
    """ModelSerializer For Blog Model"""
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = Blog
        fields = "__all__"