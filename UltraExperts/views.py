from decouple import config
from email import message
import email
from django.http import response
from django.shortcuts import render
from elasticsearch import serializer
from rest_framework_simplejwt.tokens import Token
from UltraExperts.serializers import UserSerilizer
from dj_rest_auth.views import LoginView,PasswordResetConfirmView
from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_STORAGE_BUCKET_NAME
from botocore.client import Config
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser,ParseError
from .files import *
from rest_framework.validators import ValidationError
from django.template.loader import get_template
from django.core.mail import send_mail
from twilio.rest import Client
from .constants import TWILIO_AUTH_ID,TWILIO_SECRET_KEY
from twilio.base.exceptions import TwilioRestException
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.contrib.auth import authenticate,login
from django.conf import settings
from rest_framework import status
import jwt
from rest_framework import generics
from .serializers import *


ACCESS_KEY = AWS_ACCESS_KEY_ID
SECRET_KEY = AWS_SECRET_ACCESS_KEY
BUCKET_NAME = AWS_STORAGE_BUCKET_NAME

client = Client(TWILIO_AUTH_ID, TWILIO_SECRET_KEY)



def privacy(request):
    return render(request,"privacy.html")


class CustomLoginView(LoginView):
      
    def get_user(self):
        serilize = UserSerilizer(self.request.user)
        return serilize.data
        
    def get_response(self):
        orginal_response = super().get_response()
        mydata = self.get_user()
        orginal_response.data.update(mydata)
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
            html_data = html.render({"otp":self.gen_otp,"username":email})
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
    gen_otp = random.randint(1000, 9999)
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


class MobileLogin(APIView):
    def post(self,request):
        mobile = request.data["mobile"]
        password = request.data["password"]

        user=authenticate(mobile=mobile,password=password)
        if user.is_active:
            login(request, user)
        else:
            return Response({"msg":"invelid creadential"},status=status.HTTP_200_OK)
        











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
