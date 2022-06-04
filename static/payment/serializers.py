from rest_framework import serializers
from .models import *

class PaymantStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = "__all__"