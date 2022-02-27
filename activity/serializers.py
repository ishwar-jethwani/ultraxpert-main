from rest_framework import serializers
from .models import *
from user.serializers import *
from payment.models import PaymentStatus
from events.models import *
from django.core.mail import send_mail
from django.template.loader import get_template



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

class RatingUserserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id","username","is_expert"]

class RatingSerializer(serializers.ModelSerializer):
    user_name = RatingUserserializer()
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = Ratings
        fields = '__all__'


class OrderHistorySerializer(serializers.ModelSerializer):
    user = OrderUserSerilizer()
    order_created = serializers.DateTimeField(format="%c")
    service_obj = ServiceShowSerializer()
    order_on = OrderUserSerilizer()
    class Meta:
        model = Order
        fields = "__all__"
        depth = 2

    def update(self,instance, validated_data):
        transaction = PaymentStatus.objects.get(payment_id=instance.payment_id)
        if transaction.response["payload"]["payment"]["entity"]["status"] == "authorized" or "captured":
            instance.paid = True
            instance.save(update_fields=["paid"])
            admins = User.objects.all().filter(is_superuser=True)
            for admin in admins:
                pass
            return instance

class OrderStatusSerializer(serializers.ModelSerializer):
    order_created = serializers.DateTimeField(format="%c")
    service_obj = ServiceShowSerializer()
    user = UserSerilizer()
    class Meta:
        model = Order
        fields = "__all__"
        depth = 2

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.paid = True
        instance.save()
        html = get_template("service_confirmation.html")
        html.render({"service_name":instance.service_obj.service_name,"start_time":instance.slot.start_time,"end_time":instance.slot.end_time,"duration":instance.slot.duration,"date":instance.slot.schedule.day})
        send_mail(
                from_email = None,
                recipient_list = [instance.order_on.email],
                subject ="Order Confirmation",
                html_message = html,
                message = "Service is booked"
            
        )
        send_mail(
                from_email = None,
                recipient_list = [instance.user.email],
                subject ="Order Confirmation",
                html_message = html,
                message = "Service is booked"
            
        )
        return instance


    
class OrderSerializer(serializers.ModelSerializer):
    user = OrderUserSerilizer()
    order_on = OrderUserSerilizer()
    service_obj = ServiceShowSerializer()
    order_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = Order
        fields = "__all__"
        depth = 2

    


# class SlotBookingSerializer(OrderSerializer):
#     class Meta:
#         model = EventScheduleTime
#         fields = OrderSerializer.Meta.fields



#     def update(self,instance, validated_data):
#         data = self.context["request"].data
#         if data["status"] == "booked":
#             instance.save()
#             receipt = Order.objects.create(
#                     user = self.context["request"].user,
#                     service_id = instance.schedule.event.releted_service.service_id,
#                     service_obj = instance.schedule.event.releted_service,
#                     price = instance.schedule.event.releted_service.price,
#                     order_on = instance.schedule.event.releted_service.user,
#                     slot = instance
#             )
#             if receipt:
#                 return receipt


class SubscriptionSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%c")
    class Meta:
        model = Subscriptions
        fields = "__all__"
        depth = 1
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.paid = True
        instance.save()
        return instance