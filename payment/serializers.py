from rest_framework import serializers
from .models import *

class PaymantStatusSerializer(serializers.ModelSerializer):
    """ModelSerializer For Payment Status """
    class Meta:
        model = PaymentStatus
        fields = "__all__"