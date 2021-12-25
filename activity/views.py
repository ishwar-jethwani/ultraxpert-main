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

    def get(self,request,pk):
        profile = Profile.objects.get(pk=pk)
        reviews_obj = Ratings.objects.filter(rating_on=profile)
        serialize = RatingSerializer(reviews_obj,many=True)
        return Response(serialize.data)

    def post(self,request,pk):
        data = request.data
        profile = Profile.objects.get(pk=pk)
        point = float(data["star"])
        if point>5.0:
            point = 5.0
            created = Ratings.objects.create(user_name=request.user,review=data["review"],star_rating=point,rating_on=profile)
        else:
            created = Ratings.objects.create(user_name=request.user,review=data["review"],star_rating=point,rating_on=profile)
        if created:

            pass
            return Response({"msg":f"thank you for submitting your review on {profile}"})
        else:
            return Response({"msg":"error in submitting"})



class Place_Order(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceBookingSerializer
    queryset = Services.objects.all()
    lookup_field = "service_id"


class OrderHistory(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        order_objs = Order.objects.filter(user=user)
        order_list = OrderHistorySerializer(order_objs,many=True)
        return Response(order_list.data)



class ExpertSearchView(generics.ListAPIView):
    queryset = Profile.objects.filter(profile__is_expert = True)
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["first_name","last_name","profile__username","profile__email"]


class ExpertServicesSearchView(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["service_name"]

class SearchView(APIView):
    def get(self,request):
        data = request.data["serach"]
        try:
            keyword = Keywords.objects.get(name=data)
            related_expert = Profile.objects.filter(keywords=keyword)
        except:
            category = Category.objects.get(name=data)
            related_expert = Profile.objects.filter(categories=category)
        serialize = ProfileSerializer(related_expert,many=True)
        if serialize:
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response({"msg":"we could not find any profile releted to this keyword or category"})




class ExpertDetailView(APIView):

    def get(self,request,pk):
        user = User.objects.get(pk=pk)

        profile_obj = Profile.objects.filter(Q(profile__is_expert=True) & Q(profile__user_id=user.user_id))
        social_obj = SocialMedia.objects.filter(user__user_id=user.user_id)
        service_obj = Services.objects.filter(user__user_id=user.user_id)
        rating_obj  = Ratings.objects.filter(rating_on__profile__user_id=user.user_id)
        rating_res = RatingSerializer(rating_obj,many=True)
        profile_res = ProfileSerializer(profile_obj,many=True)
        social_res  = SocialMediaSerializer(social_obj,many=True)
        service_res = ServicesSerializer(service_obj,many=True)
        user_profiles = json.dumps(profile_res.data)
        profiles = json.loads(user_profiles)
        user_services = json.dumps(service_res.data)
        services = json.loads(user_services)
        user_social_links = json.dumps(social_res.data)
        social_links = json.loads(user_social_links)

        data = json.dumps(rating_res.data)
        stars = json.loads(data)
        avg_list = list()
        for star in stars:
            avg_list.append(star["star_rating"]) 
        try:
            avg = sum(avg_list)/len(avg_list)
            count= len(avg_list)
        except ZeroDivisionError:
            avg = 0.0
            count= len(avg_list)

        profile = {"expert profile":{"personal_detail":profiles,"social":social_links,"sevices":services,"ratings":{"avg":round(avg,1),"reviews":count}}}
        return Response(profile,status=status.HTTP_200_OK)



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
    


    












    






        
        


