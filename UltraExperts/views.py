from decouple import config
from django.shortcuts import render
from UltraExperts.backends import MobileAuthenticationBackend
from UltraExperts.serializers import UserSerilizer
from dj_rest_auth.views import LoginView
from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_STORAGE_BUCKET_NAME
from rest_framework.parsers import FileUploadParser,ParseError
from .files import *
from rest_framework.validators import ValidationError
from django.template.loader import get_template
from django.core.mail import send_mail
from twilio.rest import Client
from .constants import BASE_URL, TWILIO_AUTH_ID,TWILIO_SECRET_KEY
from twilio.base.exceptions import TwilioRestException
from django.contrib.auth import authenticate
from rest_framework import status
import jwt
from .serializers import *
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from allauth.socialaccount.providers.linkedin_oauth2.views import LinkedInOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter




ACCESS_KEY = AWS_ACCESS_KEY_ID
SECRET_KEY = AWS_SECRET_ACCESS_KEY
BUCKET_NAME = AWS_STORAGE_BUCKET_NAME

client = Client(TWILIO_AUTH_ID, TWILIO_SECRET_KEY)



def privacy(request):
    return render(request,"privacy.html")

class CreatSuperuserAPI(APIView):
    def post(self,request):
        self.username = request.data["username"]
        self.email = request.data["email"]
        password = request.data["password"]
        user = User(
        username = self.username,
        email = self.email,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        serialize = UserSerilizer(user)
        return Response(serialize.data,status=status.HTTP_201_CREATED)

class CustomLoginView(LoginView):
      
    def get_user(self):
        serilize = UserSerilizer(self.request.user)
        return serilize.data
        
    def get_response(self):
        orginal_response = super().get_response()
        mydata = self.get_user()
        orginal_response.data.update(mydata)
        email = mydata["email"]
        username = mydata["username"]
        subject = "Ultra Creation Sending Email"
        message = "Hi %s! Welcome to UltraXpert" % email
        htmly = get_template("welcome-email.html")
        htmly = htmly.render({"username":username})
        User.objects.filter(email=email).update(is_verified=True)
        send_mail(
            from_email = None,
            recipient_list = [email],
            subject =subject,
            html_message = htmly,
            message = message
            )

        return orginal_response 


class MobileUserCreate(APIView):
    def post(self,request):
        mobile = request.data["mobile"]
        password1 = request.data["password1"]
        password2 = request.data["password2"]
        username = request.data["username"]
        if password1==password2:
            password = password2
            user = User.objects.filter(mobile=mobile)
            if user.exists():
                return Response({"msg":"user is already exist"},status=status.HTTP_400_BAD_REQUEST)
            else:
                user_register = User.objects.create_mobile_user(mobile,password,username)
                serialize = UserSerilizer(user_register)
                if user_register:
                    return Response({"msg":"user is sucessfully created","user":serialize.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({"msg":"invelid request"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"password is not match"},status=status.HTTP_400_BAD_REQUEST)
        
        




#email otp verification
class UserEmailVerification(APIView):
    gen_otp = random.randint(1000,9999)
    def post(self,request):
        email = request.data["email"]
        user = User.objects.filter(email=email)
        if user.exists():
            return Response({"msg":"email address is already exist please try with diferent email address"},status=status.HTTP_400_BAD_REQUEST)
        else:
            html = get_template("email.html")
            html_data = html.render({"otp":self.gen_otp})
            key = config("KEY_FOR_OTP")
            encoded_value = jwt.encode({"otp":self.gen_otp},key,algorithm="HS256")
            send_mail(
                from_email = None,
                recipient_list = [email],
                subject="UltraXpert Email Verification",
                html_message=html_data,
                message="You are most Welcome"
            )
            return Response({"msg":"email has been sent","value":encoded_value},status=status.HTTP_200_OK)
    

    # def post(self,request):
    #     data = request.data
    #     otp = data["otp"]
    #     if str(otp) == str(self.gen_otp):
    #         return Response({"msg":"email is verified"},status=status.HTTP_200_OK)
    #     else:
    #         raise ValidationError(detail="You have enterd wrong otp", code=400) # raise error ok 


# forgot password
class ResetPassword(APIView):
    gen_otp = random.randint(100000,999999)
    user = User()
    def get(self,request):
        self.email = request.GET.get("email")
        self.user = User.objects.get(email=self.email)
        if self.user:
            email = self.user.email
            if self.email == email:
                html = get_template("reset.html")
                html_data = html.render({"otp":self.gen_otp})
                send_mail(
                from_email = None,
                recipient_list = [email],
                subject ="Reset Your Password",
                html_message=html_data,
                message = f"This is you otp:{self.gen_otp} to reset your password"
                )
                return Response({"msg":"email has been sent"},status=status.HTTP_200_OK)
            return Response({"msg":"email is failed to send"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"msg":"You Are Not In Our Database"},status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        data = request.data
        otp = data["otp"]
        password = data["password"]
        password_confirm = data["password_confirm"]
        self.email = data["email"]
        self.user = User.objects.get(email=self.email)
        if str(otp) == str(self.gen_otp):
            if password == password_confirm:
                self.user.set_password(password)
                self.user.save()
                return Response({"msg":"password is set sucessfully"},status=status.HTTP_200_OK)
        return Response({"msg":"you have entered wrong otp"})

#  password reste by mobile otp
class MobileResetPassword(APIView):
    gen_otp = random.randint(1000, 9999)
    user = User()
    def get(self,request):
        self.mobile = request.GET.get("mobile_number")
        self.user = User.objects.get(mobile=self.mobile)
        mobile = self.user.mobile
        if self.mobile == mobile:
            try:
                client.messages.create(to=mobile, from_="+19124915017",
                                    body="Thank you for visiting and we need lititle more information to complete your registration plese enter the {} to verify your mobile number to change password ".format(self.gen_otp))
            except TwilioRestException as e:
                print(e)
            return Response({"msg":"msg has been sent"},status=status.HTTP_200_OK)
        return Response({"msg":"msg is failed to send"})

    def post(self,request):
        data = request.data
        self.mobile = data["mobile"]
        otp = data["otp"]
        password = data["password"]
        password_confirm = data["password_confirm"]
        self.user = User.objects.get(mobile=self.mobile)
        if str(otp) == str(self.gen_otp):
            if password == password_confirm:
                self.user.set_password(password)
                self.user.save()
                return Response({"msg":"password is set sucessfully"},status=status.HTTP_200_OK)
        return Response({"msg":"you have entered wrong otp"})



# mobile verification
class MobileVerificationApi(APIView):
    gen_otp = random.randint(1000,9999)
    def post(self,request):
        mobile = request.data["mobile"]
        user = User.objects.filter(mobile=mobile)
        if user.exists():
            return Response({"msg":"mobile number is already exist please try with diferent mobile number"},status=status.HTTP_400_BAD_REQUEST)
        else:
            key = config("KEY_FOR_OTP")
            encoded_value = jwt.encode({"otp":self.gen_otp},key,algorithm="HS256")
            try:
                client.messages.create(to=mobile, from_="+19124915017",
                                    body="Thank you for visiting and we need lititle more information to complete your registration plese enter the {} to verify your mobile number ".format(self.gen_otp))
            except TwilioRestException as e:
                print(e)
            return Response({"msg":"msg is failed to send","value":encoded_value},status=status.HTTP_200_OK)

# mobile login
class MobileLogin(APIView):
    user_dict = dict()
    def post(self,request):
        mobile = request.data["mobile"]
        password = request.data["password"]
        user=authenticate(mobile=mobile,password=password)
        print(user)
        if user is not None:
            if user.is_active:
                data = RefreshToken.for_user(user)
                serialize = UserSerilizer(user)
                self.user_dict.update(serialize.data)
                self.user_dict.update({"access_token":str(data)})
                self.user_dict.update({"refresh_token":str(data.access_token)})
                return Response(self.user_dict,status=status.HTTP_200_OK)   
        else:
            return Response({"msg":"invelid creadential"},status=status.HTTP_400_BAD_REQUEST)
        

class FileUploadView(APIView):
    parser_class = [FileUploadParser]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if "file" not in request.data:
            raise ParseError("FIle should be provided")
        file_obj = request.data["file"]
        filetype = request.data["filetype"]
        name = request.data["name"]
        try:
            url, ext = upload(file_obj, filetype, name)
        except Exception as e:
            raise ValidationError(detail="Unable to upload file. Reason - {}".format(e), code=400)
        return Response(
            {
                "status": True,
                "message": "File Uploaded",
                "url": url,
            },
            status=201,
        )



class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = BASE_URL+"/accounts/google/login/callback/"
    client_class = OAuth2Client

class LinkedInLogin(SocialLoginView):
    adapter_class = LinkedInOAuth2Adapter
    callback_url = BASE_URL+"/accounts/linkedin/login/callback/"    
    client_class = OAuth2Client


class CheckPromocode(APIView):
    def get(self,request):
        promocode = request.GET.get("promocode")
        if User.objects.filter(refer_code=promocode).exists():
            return Response({"status":True},status=status.HTTP_200_OK)
        else:
            return Response({"status":False},status=status.HTTP_200_OK)
