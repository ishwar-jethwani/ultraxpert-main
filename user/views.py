from ast import Return
from UltraExperts.serializers import UserSerilizer
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
import json
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from UltraExperts.constants import DEBUG
from django.db.models import Q

#View For Home View 

class Home_View(APIView):
    """Displaying Home Page"""
    def get(self,request):
        page_number = 1
        user = []
        number = 51
        if DEBUG == False:
            user = User.objects.filter(is_expert=True,is_verified=True)
            if user.count()<number:
                number = user.count()
        else:
            user = User.objects.filter(is_expert=True)
        user = Paginator(user,number)
        user = user.page(int(page_number))
        expert_list = []
        for i in user:
            profile_obj = Profile.objects.filter(profile__user_id=i.user_id)
            rating_obj  = Ratings.objects.filter(rating_on__profile__user_id=i.user_id)
            rating_res = RatingSerializer(rating_obj,many=True)
            profile_res = ProfileSerializer(profile_obj,many=True)
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
            profile = {"expert_profile":{"personal_detail":profile_res.data,"ratings":{"avg":round(avg,1),"reviews":count}}}
            expert_list.append(profile)
        return Response({"experts":expert_list},status=status.HTTP_200_OK)


#View For User Plan

class UserPlanSelect(APIView):
    """User Plan Selection"""
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data = UserPlans.objects.all()
        serialize = UserPlanSerilizer(data,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    def post(self,request):
        user = request.user
        plan = request.data["select_plan"]
        plan_selection = UserPlans.objects.get(pk=plan)
        user_profile = Profile.objects.filter(profile=user)
        plan_selected = user_profile.update(user_plan=plan_selection)
        if plan_selected:
            User.objects.filter(user_id = user.user_id).update(is_expert=True)
            subscription = Subscriptions.objects.create(
                plan = plan_selection,
                user = user
            )
            if subscription:
                serialize = SubscriptionSerializer(subscription)
                return Response(data=serialize.data,status=status.HTTP_200_OK)
        return Response(data={"msg":"somthing went wrong"},status=status.HTTP_400_BAD_REQUEST)

#View For Expert Page 

class Expert_View(APIView):
    """Displaying Expert Home Page"""
    def get(self,request):
        page_number = 1
        user = []
        number  = 30
        if "page" in  request.GET:
            page_number = request.GET["page"]
        if DEBUG == False:
            user = User.objects.filter(is_expert=True,is_verified=True)
            if user.count()<number:
                number = user.count()
        else:
            user = User.objects.filter(is_expert=True)
        user = Paginator(user,number)
        user = user.page(int(page_number))
        expert_list = []
        for i in user:
            profile_obj = Profile.objects.filter(profile__user_id=i.user_id)
            rating_obj  = Ratings.objects.filter(rating_on__profile__user_id=i.user_id)
            rating_res = RatingSerializer(rating_obj,many=True)
            profile_res = ProfileSerializer(profile_obj,many=True)
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
            profile = {"expert_profile":{"personal_detail":profile_res.data,"ratings":{"avg":round(avg,1),"reviews":count}}}
            expert_list.append(profile)
        return Response({"experts":expert_list},status=status.HTTP_200_OK)

#View For Auto Completion Of Profile

class AutoCompleteAPIView(APIView):
    """Profile Auto Complete"""
    def get(self,request):
        search = ""
        if "search" in request.GET:
            search = request.GET.get("search")
        try:
            # user = User.objects.filter(is_expert=True,)
            profile_obj = Profile.objects.filter(profile__is_expert=True).filter(Q(first_name__icontains=search)|Q(last_name__icontains=search))
            service_obj = Services.objects.filter(service_name__icontains=search)
            data = []
            if profile_obj.exists():
                profile_res = ProfileAutoCompleteSerializer(profile_obj,many=True)
                data = profile_res.data
            elif service_obj.exists():
                service_res = ServiceAutoCompleteSerializer(service_obj,many=True)
                data = service_res.data
            elif profile_obj.exists() and service_obj.exists():
                profile_res = ProfileAutoCompleteSerializer(profile_obj,many=True)
                service_res = ServiceAutoCompleteSerializer(service_obj,many=True)
                profile_data = profile_res.data
                service_data = service_res.data
                data = profile_data+service_data
            return Response(data=data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":e},status=status.HTTP_400_BAD_REQUEST)

#View For Deleting User

class UserDelete(APIView):
    """User Deletion"""
    permission_classes = [IsAuthenticated]
    serializer_class   = UserSerilizer
    def delete(self,request):
        user = request.user
        object = User.objects.get(user_id=user.user_id)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#View For Profile View

class Profile_View(generics.RetrieveUpdateAPIView):
    """"Displaying Profile"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        queryset = Profile.objects.filter(profile=user)
        obj = queryset.first()
        return obj

#View For Dispalying Category

class CategoryAPIView(generics.ListCreateAPIView):
    """Listing Category"""
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

#View For modifying Category

class CategoryRetriveAPIView(generics.RetrieveUpdateDestroyAPIView):
    """"Category Modification"""
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"

#View For Dispalying Service

class ServiceCreate(generics.ListCreateAPIView):
    """"Listing Service"""
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)

#View For Updating Service
   
class ServiceUpdate(generics.UpdateAPIView):
    """"Updating Service"""
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    lookup_field = "service_id"
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)

#View For Deleting Service

class ServiceDelete(generics.DestroyAPIView):
    """Deletion Of Service"""
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    lookup_field = "service_id"
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)

#View For Dispalying Service

class ServiceDetail(generics.RetrieveAPIView):
    """"Service Detail Fetching"""
    serializer_class = ServiceShowSerializer
    lookup_field = "service_id"
    queryset = Services.objects.all()
    
#View For Dispalying ServiceList

class ServiceList(generics.ListAPIView):
    """"Listing Service List"""
    serializer_class = ServiceShowSerializer
    def get_queryset(self):
        page_number = 1
        if "page" in  self.request.GET:
            page_number = self.request.GET["page"]
        services = Services.objects.all()
        services = Paginator(services,10)
        services = services.page(int(page_number))
        return services


# class ServiceList(APIView):
#     def get(self,request):
#         page_number = 1
#         if "page" in  request.GET:
#             page_number = request.GET["page"]
#         services = Services.objects.all()
#         services = Paginator(services,10)
#         services = services.page(int(page_number))
#         serialize = ServiceShowSerializer(services)
#         return Response(serialize.data,status=status.HTTP_200_OK)
    
#Listing User Plan

class UserPlanAPIView(generics.ListAPIView):
    """"Listing User Plan"""
    serializer_class = UserPlanSerilizer
    queryset = UserPlans.objects.all()

#Listing User Plan

class KeywordsAPIView(generics.ListCreateAPIView):
    """"Listing Keywords"""
    permission_classes = [IsAuthenticated]
    serializer_class = KeywordSerilizer
    queryset = Keywords.objects.all()

#Updating User Plan

class UserUpdateAPI(generics.RetrieveUpdateAPIView):
    """"Updation Of Users plan"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerilizer
    queryset = User.objects.all()
    lookup_field = "user_id"

#View For Expert Detail View

class ExpertDetailView(APIView):
    """Expert Details """
    def get(self,request,user_id):
        user = User.objects.get(user_id=user_id)
        profile_obj = Profile.objects.filter(profile__is_expert=True,profile=user)
        service_obj = Services.objects.filter(user=user)
        rating_obj  = Ratings.objects.filter(rating_on__profile=user)
        rating_res = RatingSerializer(rating_obj,many=True)
        profile_res = ProfileSerializer(profile_obj,many=True)
        service_res = ServiceShowSerializer(service_obj,many=True)
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

        profile = {"expert_profile":{"personal_detail":profile_res.data,"sevices":service_res.data,"ratings":{"avg":round(avg,1),"reviews":count}}}
        return Response(profile,status=status.HTTP_200_OK)

#View For Creating Bank Details 

class BankDetailCreate(generics.CreateAPIView):
    """Creating Bank Details"""
    permission_classes = [IsAuthenticated]
    serializer_class = BankSerializer
    def get_queryset(self):
        return BankDetail.objects.filter(user=self.request.user)

#View For Reading Bank Details

class BankDetailRead(generics.RetrieveUpdateAPIView):
    """"Retrieving Bank Details"""
    permission_classes = [IsAuthenticated]
    serializer_class = BankSerializer
    def get_object(self):
        object = BankDetail.objects.filter(user=self.request.user).first()
        return object

#View For Displaying Comments 

class CommentAPIView(APIView):
    """"Displaying Comments"""
    permission_classes = [IsGETOrIsAuthenticated]
    serializer_class = ServicesSerializer

    def get(self,request,service_id):
        comment_id = request.GET["comment_id"]
        main_comments= Comment.objects.filter(service__service_id=service_id)
        if main_comments.exists():
            if comment_id is not None:
                main_comments= Comment.objects.filter(service__service_id=service_id,reply__id=comment_id)
            serialize = CommentSerializer(main_comments,many=True)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        return Response(data=[],status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,service_id):
        try:
            user = request.user
            comment_msg = request.data["messgae"]
            service = Services.objects.get(service_id=service_id)
            comment_obj = Comment.objects.create(service=service,user=user,comment=comment_msg)
            if "comment_id" in request.data:
                comment_obj_first = Comment.objects.filter(id=request.data["comment_id"])
                if comment_obj_first.exists():
                    self_obj = comment_obj_first.first()
                    comment_obj = Comment.objects.create(service=service,user=user,comment=comment_msg,reply=self_obj)
            comment = CommentSerializer(comment_obj)
            return Response(comment.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"msg":e},status=status.HTTP_400_BAD_REQUEST)



                

        








