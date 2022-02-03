from django.db.models.fields import related
from user.serializers import *
from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import json
from rest_framework import filters
from user.models import *
from rest_framework import permissions


class IsGETOrIsAuthenticated(permissions.BasePermission):        

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        return request.user and request.user.is_authenticated

class SendProjectRequest(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = ProjectRequestSerializer
    def get_queryset(self):
        return Project_Request.objects.filter(request_from_user=self.request.user)


class AcceptAndRejectProjectRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,request_id):
        project_request = Project_Request.objects.get(request_id=request_id)
        profile = Profile.objects.get(profile=project_request.request_to_profile)
        if project_request.request_to_profile == profile:
            project_request.request_to_profile.got_projects.add(project_request)
            return Response({"msg":"project accepted"})
        else:
            project_request.delete()
            return Response({"msg":"project rejected"})




class RatingView(APIView):
    permission_classes = [IsGETOrIsAuthenticated]

    def get(self,request,user_id):
        profile = Profile.objects.get(profile__user_id=user_id)
        reviews_obj = Ratings.objects.filter(rating_on=profile)
        serialize = RatingSerializer(reviews_obj,many=True)
        return Response(serialize.data)

    def post(self,request,user_id):
        data = request.data
        profile = Profile.objects.get(profile__user_id=user_id)
        point = float(data["star"])
        if point>5.0:
            point = 5.0
            created = Ratings.objects.create(user_name=request.user,review=data["review"],short_title=data["short_title"],star_rating=point,rating_on=profile)
        else:
            created = Ratings.objects.create(user_name=request.user,review=data["review"],short_title=data["short_title"],star_rating=point,rating_on=profile)
        if created:

            pass
            return Response({"msg":f"thank you for submitting your review on {profile}"})
        else:
            return Response({"msg":"error in submitting"})



# class Place_Order(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SlotBookingSerializer
#     queryset = Event.objects.all()
#     lookup_field = "event_id"


class Place_Order(APIView):
    permission_classes= [IsAuthenticated]
    def post(self,request,service_id):
        user = request.user
        event_id = request.data["event_id"]
        service  = Services.objects.get(service_id=service_id)
        event_slot = EventScheduleTime.objects.get(id=event_id)
        order = Order.objects.create(user=user,service_id=service.service_id,slot=event_slot,service_obj=service,price=service.price,order_on=service.user)
        if order:
            serialize = OrderSerializer(order)
            return Response(serialize.data,status=status.HTTP_200_OK)
        else:
            return Response({"msg":"somthing went wrong"},status=status.HTTP_200_OK)
        





        







class OrderHistory(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        order_objs = Order.objects.filter(user=user)
        order_list = OrderHistorySerializer(order_objs,many=True)
        return Response(order_list.data)




class PaymentConfirmationApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderHistorySerializer
    lookup_field = "order_id"


class OrderStatusUpdateApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    lookup_field = "order_id"

        
class ExpertGotOrder(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderHistorySerializer
    def get_queryset(self):
        return Order.objects.filter(order_on=self.request.user)



class SubscriptionView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    def get_queryset(self):
        return Subscriptions.objects.filter(user=self.request.user)
    


    












    






        
        


