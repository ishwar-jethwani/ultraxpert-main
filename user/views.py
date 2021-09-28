from UltraExperts.serializers import UserSerilizer
from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import *
from .serializers import *
import json
from activity.serializers import RatingSerializer,SubscriptionSerializer
from activity.models import Ratings
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialConnectView
from rest_auth.social_serializers import TwitterConnectSerializer
from activity.views import IsGETOrIsAuthenticated
from activity.models import Subscriptions
import requests
import json



class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter

class TwitterConnect(SocialConnectView):
    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter




class UserPlanSelect(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data = User_Plans.objects.all()
        serialize = UserPlanSerilizer(data,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    def post(self,request):
        print("come inpost request")
        user = request.user
        plan = request.data["select_plan"]
        plan_selection = User_Plans.objects.get(pk=plan)
        user_profile = Profile.objects.filter(profile=user)
        plan_selected = user_profile.update(user_plan=plan_selection)
        if plan_selected:
            usr = User.objects.filter(user_id=user.user_id)
            usr.update(is_expert=True)
            subscription = Subscriptions.objects.create(
                plan = plan_selection,
                user = user
            )
            if subscription:
                serialize = SubscriptionSerializer(subscription)
                
                return Response(data=serialize.data,status=status.HTTP_200_OK)
            return Response(data={"msg":"somthing went wrong"},status=status.HTTP_400_BAD_REQUEST)

class Expert_View(APIView):

    def get(self,request):
        user = User.objects.all()
        expert_list = []
        for i in user:
            profile_obj = Profile.objects.filter(Q(profile__is_expert=True) & Q(profile__user_id=i.user_id))
            social_obj = SocialMedia.objects.filter(user__user_id=i.user_id)
            service_obj = Services.objects.filter(user__user_id=i.user_id)
            rating_obj  = Ratings.objects.filter(rating_on__profile__user_id=i.user_id)
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
            profile = {"expert profile":{"personal_detail":profiles,"social":social_links,"services":services,"ratings":{"avg":avg,"reviews":count}}}
            expert_list.append(profile)
        return Response({"experts":expert_list})




class UserDelete(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = UserSerilizer
    def delete(self,request):
        user = request.user
        object = User.objects.get(user_id=user.user_id)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Profile_View(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(profile=user)

class SocialMedia_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data
        users = User.objects.all()
        for user in users:
            if request.user.user_id == user.user_id:
                created = SocialMedia.objects.create(
                    user = request.user,
                    icon = data["icon"],
                    plateform_name = data["plateform_name"],
                    link = data["link"]
                )
                serialize = SocialMediaSerializer(created)
                data = json.dumps(serialize.data)
                resp = json.loads(data)
                if created:
                    return Response(resp,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class SocialMediaLinks(APIView):
    def get(self,request,user_id):
        social_obj = SocialMedia.objects.filter(user__user_id=user_id)
        serialize = SocialMediaSerializer(social_obj,many=True)
        return Response(serialize.data)

class CategoryAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryRetriveAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"

class ServiceCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)
    
class ServiceRetriveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    lookup_field = "pk"
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)

class UserPlanAPIView(generics.ListAPIView):
    serializer_class = UserPlanSerilizer
    queryset = User_Plans.objects.all()

class KeywordsAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KeywordSerilizer
    queryset = Keywords.objects.all()

class UserUpdateAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerilizer
    queryset = User.objects.all()
    lookup_field = "user_id"



        




        