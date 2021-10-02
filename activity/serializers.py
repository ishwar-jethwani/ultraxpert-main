from django.db.models import fields
from rest_framework import request, serializers
from .models import *
from user.serializers import *
from payment.models import PaymentStatus
import requests

class ProjectRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Request
        fields = "__all__"
    
    def create(self, validated_data):
        validated_data.pop("request_from_user")
        user = self.context["request"].user
        service = Services.objects.get(service_id=validated_data.get("service_id"))
        profile =   Profile.objects.get(profile=service.user)
        request = Project_Request.objects.create(
            request_from_user = user,
            service = service,
            request_to_profile = profile
        )
        return request

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'
        depth = 1


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1

    def update(self,instance, validated_data):
        transaction = PaymentStatus.objects.get(payment_id=instance.payment_id)
        if transaction.response["payload"]["payment"]["entity"]["status"] == "authorized":
            instance.paid = True
            admins = User.objects.all().filter(is_superuser=True)
            for admin in admins:
                pass
            return instance

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["user","service_id","price"]

    


class ServiceBookingSerializer(OrderSerializer):
    class Meta:
        model = Services
        fields = OrderSerializer.Meta.fields



    def update(self,instance, validated_data):
        data = self.context["request"].data
        if data["status"] == "booked":
            instance.ordered = True
            instance.save()
            receipt = Order.objects.create(
                    user = self.context["request"].user,
                    service_id = instance.service_id,
                    service_obj = instance,
                    price = instance.price,
                    order_on = instance.user

            )
            if receipt:
                return receipt


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = "__all__"
        depth = 1