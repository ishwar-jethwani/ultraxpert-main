from email import message
import email
from django.shortcuts import render
from requests.api import post
from rest_framework_simplejwt.tokens import Token
from UltraExperts.serializers import UserSerilizer
from dj_rest_auth.views import LoginView,PasswordResetConfirmView
from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import random
from .settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_STORAGE_BUCKET_NAME
from botocore.client import Config
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser,ParseError
from .files import *
from rest_framework.validators import ValidationError
from django.template.loader import get_template
from django.core.mail import send_mail
import requests
import json
from twilio.rest import Client
from .constants import TWILIO_AUTH_ID,TWILIO_SECRET_KEY
from twilio.base.exceptions import TwilioRestException
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status

ACCESS_KEY = AWS_ACCESS_KEY_ID
SECRET_KEY = AWS_SECRET_ACCESS_KEY
BUCKET_NAME = AWS_STORAGE_BUCKET_NAME

client = Client(TWILIO_AUTH_ID, TWILIO_SECRET_KEY)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# class LoginView(APIView):
#     def post(self, request, format=None):
#         data = request.data
#         response = Response()        
#         email = data.get('email', None) 
#         password = data.get('password', None)
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             if user.is_active:
#                 data = get_tokens_for_user(user)
#                 response.set_cookie(
#                     key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
#                     value = data["access"],
#                     expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
#                     secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                     httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                     samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#                 )
#                 csrf.get_token(request)
#                 response.data = {"Success" : "Login successfully","data":data}
#                 return response
#             else:
#                 return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)






def privacy(request):
    return render(request,"privacy.html")

# def set_cookie(response, key, value):
#     if days_expire is None:
#         max_age = 365 * 24 * 60 * 60  # one year
#     else:
#         max_age = days_expire * 24 * 60 * 60
#     expires = datetime.datetime.strftime(
#         datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
#         "%a, %d-%b-%Y %H:%M:%S GMT",
#     )
#     response.set_cookie(
#         key,
#         value,
#         max_age=max_age,
#         expires=expires,
#         domain=settings.SESSION_COOKIE_DOMAIN,
#         secure=settings.SESSION_COOKIE_SECURE or None,
#     )

    




class CustomLoginView(LoginView):
      
    def get_user(self):
        serilize = UserSerilizer(self.request.user)
        return serilize.data
        
    def get_response(self):
        orginal_response = super().get_response()
        mydata = self.get_user()
        orginal_response.data.update(mydata)
        data = get_tokens_for_user(self.request.user)
        orginal_response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
            value = data["access"],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        csrf.get_token(self.request)
        email = mydata["email"]
        subject = "Ultra Creation Sending Email"
        message = "Hi %s! Welcome to UltraXpert" % email
        htmly = get_template("welcome.html")
        htmly = htmly.render({"username":email})
        User.objects.filter(email=email).update(is_verified=True)
        send_mail(
            from_email = None,
            recipient_list = [email],
            subject =subject,
            html_message = htmly,
            message = message
            )

        return orginal_response 




#email otp verification
class UserEmailVerification(APIView):
    gen_otp = random.randint(100000,999999)
    def get(self,request):
        email = request.data["email"]
        user = User.objects.filter(email=email)
        if user.exists():
            return Response({"msg":"email address is already exist please try with diferent email address"},status=status.HTTP_400_BAD_REQUEST)
        else:
            html = get_template("email.html")
            html_data = html.render({"otp":self.gen_otp,"username":email})
            send_mail(
                from_email = None,
                recipient_list = [email],
                subject="UltraXpert Email Varification",
                html_message=html_data
            )
            return Response({"msg":"email has been sent"},status=status.HTTP_200_OK)
    

    def post(self,request):
        data = request.data
        otp = data["otp"]
        if str(otp) == str(self.gen_otp):
            return Response({"msg":"email is verified"},status=status.HTTP_200_OK)
        else:
            raise ValidationError(detail="You have enterd wrong otp", code=400) # raise error ok 


# forgot password
class ResetPassword(APIView):
    gen_otp = random.randint(100000,999999)
    user = User()
    def get(self,request):
        user_email = request.data["email"]
        self.user = User.objects.get(email=user_email)
        email = self.user.email
        if user_email == email:
            send_mail(
            from_email = None,
            recipient_list = [email],
            subject ="Reset Your Password",
            message = f"This is you otp:{self.gen_otp} to reset your password"

            )
            return Response({"msg":"email has been sent"},status=status.HTTP_200_OK)
        return Response({"msg":"email is failed to send"})

    def post(self,request):
        data = request.data
        otp = data["otp"]
        password = data["password"]
        password_confirm = data["password_confirm"]
        
        if str(otp) == str(self.gen_otp):
            if password == password_confirm:
                self.user.set_password(password)
                return Response({"msg":"password is set sucessfully"},status=status.HTTP_200_OK)
        return Response({"msg":"you have entered wrong otp"})

#  password reste by mobile otp
class MobileResetPassword(APIView):
    gen_otp = random.randint(100000, 999999)
    user = User()
    def get(self,request):
        user_mobile = request.data["mobile_number"]
        self.user = User.objects.get(mobile=user_mobile)
        mobile = self.user.mobile
        if user_mobile == mobile:
            return Response({"msg":"msg has been sent"},status=status.HTTP_200_OK)
        return Response({"msg":"msg is failed to send"})

    def post(self,request):
        data = request.data
        otp = data["otp"]
        password = data["password"]
        password_confirm = data["password_confirm"]
        
        if str(otp) == str(self.gen_otp):
            if password == password_confirm:
                self.user.set_password(password)
                return Response({"msg":"password is set sucessfully"},status=status.HTTP_200_OK)
        return Response({"msg":"you have entered wrong otp"})



# mobile verification
class MobileVerificationApi(APIView):
    permission_classes = [IsAuthenticated]
    gen_otp = random.randint(100000,999999)
    def get(self,request):
        user = request.user
        mobile = user.mobile
        return Response({"msg":"msg is failed to send"})
    def post(self,request):
        user = User.objects.filter(user_id=request.user.user_id)
        data = request.data
        otp = data["otp"]
        if str(otp) == str(self.gen_otp):
            user.update(is_verified=True)
            return Response({"msg":"mobile is verified"},status=status.HTTP_200_OK)
        return Response({"msg":"you have entered wrong otp"})




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
