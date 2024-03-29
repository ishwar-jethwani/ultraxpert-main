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
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from UltraExperts.constants import DEBUG
from django.db.models import Q
import random
from django.db import IntegrityError

class Home_View(APIView):
    """APIView For Displaying All Details Of User"""
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



class UserPlanSelect(APIView):
    """APIView For Selecting User Plan"""
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


class UserReporterGenrator(APIView):
    """User Report After Test"""
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        data = request.data
        qualified = data["qualified"]
        correct_ans_count = data["correct_ans_count"]
        try:
            user_report = UserTestReport.objects.create(
                user = user,
                qualified=qualified,
                correct_ans_count=correct_ans_count
            )
            serilize = UserTestReportSerializer(user_report)
            return Response(data=serilize.data,status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"msg":"Report is alredy Created!","error_msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
        finally:
            return Response({"msg":"Somthing Went Wrong"},status=status.HTTP_400_BAD_REQUEST)


class TestView(APIView):
    """Test Questions"""
    def get(self,request):
        category_name = request.GET.get("category_name")
        questions = Test.objects.filter(test_category=category_name)
        if questions.exists():
            serialize = TestSerializer(questions,many=True)
            return Response(serialize.data,status=status.HTTP_200_OK)
        else:
            return Response({"msg":"data not found"},status=status.HTTP_404_NOT_FOUND)
        


class BecomeExpertView(APIView):
    """Test Resport Check and User Converted into Expert"""
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        report = UserTestReport.objects.get(user=user)
        if report.qualified==True:
            user.is_expert=True
            user.save()
            serialize = UserSerilizer(user)
            return Response(data=serialize.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data={"msg":"Better Luck Next Time!"},status=status.HTTP_200_OK)


class Expert_View(APIView):
    """APIView For Displaying Expert Details"""
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


class AutoCompleteAPIView(APIView):
    """APIView For Auto Completing User Profile"""
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



class UserDelete(APIView):
    """APIView For Deleting User"""
    permission_classes = [IsAuthenticated]
    serializer_class   = UserSerilizer
    def delete(self,request):
        user = request.user
        object = User.objects.get(user_id=user.user_id)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Profile_View(generics.RetrieveUpdateAPIView):
    """Retrieve and Update APIView For Updating Profiles"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        queryset = Profile.objects.filter(profile=user)
        obj = queryset.first()
        return obj

class CategoryAPIView(generics.ListCreateAPIView):
    """Create APIView for Creating New Category"""
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryRetriveAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve Update APIView For Displaying Category"""
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"


class ServiceCreate(generics.ListCreateAPIView):
    """Create APIView For Creating New Service """
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)
    
class ServiceUpdate(generics.UpdateAPIView):
    """Update APIView For Updating Service """
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    lookup_field = "service_id"
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)

class ServiceDelete(generics.DestroyAPIView):
    """Destroy APIView For Deleting Service """
    permission_classes = [IsAuthenticated]
    serializer_class = ServicesSerializer
    lookup_field = "service_id"
    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)

class ServiceDetail(generics.RetrieveAPIView):
    """Retrieve APIView For Displaying Service Details"""
    serializer_class = ServiceShowSerializer
    lookup_field = "service_id"
    queryset = Services.objects.all()

class ServiceList(generics.ListAPIView):
    """List APIView for Displaying UserPlan"""
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
    

class UserPlanAPIView(generics.ListAPIView):
    """List APIView for Displaying UserPlan"""
    serializer_class = UserPlanSerilizer
    queryset = UserPlans.objects.all()

class KeywordsAPIView(generics.ListCreateAPIView):
    """Create APIView For Creating Keywords"""
    permission_classes = [IsAuthenticated]
    serializer_class = KeywordSerilizer
    queryset = Keywords.objects.all()

class UserUpdateAPI(generics.RetrieveUpdateAPIView):
    """Retrieve Update APIView For Updating User Details"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerilizer
    queryset = User.objects.all()
    lookup_field = "user_id"


class ExpertDetailView(APIView):
    """API View For Fetching Expert Details"""
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


class BankDetailCreate(generics.CreateAPIView):
    """Create APIView For Bank Detail"""
    permission_classes = [IsAuthenticated]
    serializer_class = BankSerializer
    def get_queryset(self):
        return BankDetail.objects.filter(user=self.request.user)

class BankDetailRead(generics.RetrieveUpdateAPIView):
    """Retrieve Update APIView For Bank Detail"""
    permission_classes = [IsAuthenticated]
    serializer_class = BankSerializer
    def get_object(self):
        object = BankDetail.objects.filter(user=self.request.user).first()
        return object

class CommentAPIView(APIView):
    """API For Comment"""
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

class UserTestAPI(APIView):
    """User Test Api For Creating Test"""
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        category = Profile.objects.get(profile=user).title
        questions = random.choices(Test.objects.filter(test_category=category))
        serialize = TestSerializer(questions[0:5],many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    def post(self,request):
        user = request.user
        answer = request.data["answer"]
        test_id = request.data["test_id"]
        try:
            report = UserTestReport.objects.create(user=user)
            test = Test.objects.get(test_id=test_id)
            if answer == [key for key,val in test.answers.items() if val==True][0]:
                report.correct_ans_count+=1
            elif report.correct_ans_count>=3:
                report.qualified = True
            report.save()
            serialize = UserTestReportSerializer(report)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg":"Somthing went wrong","error_message":str(e)},status=status.HTTP_400_BAD_REQUEST)

        
        

                
                
        
            
            


        


        
        



    