from email import message
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



ACCESS_KEY = AWS_ACCESS_KEY_ID
SECRET_KEY = AWS_SECRET_ACCESS_KEY
BUCKET_NAME = AWS_STORAGE_BUCKET_NAME


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
        message = "Hi %s! Testing the email functionality" % email
        htmly = get_template("email.html")


        send_mail(

            from_email = None,
            recipient_list = [email],
            subject =subject,
            #html_message = htmly,
            message = message


            )

        return orginal_response 


#email otp verification
class UserEmailVerification(APIView):
    permission_classes = [IsAuthenticated]
    gen_otp = random.randint(100000,999999)
    def get(self,request):
        user = User.objects.get(user_id=request.user.user_id)
        email = user.email
        return Response({"msg":"email has been sent"})
    

    def post(self,request):
        user = User.objects.filter(user_id=request.user.user_id)
        data = request.data
        otp = data["otp"]
        if str(otp) == str(self.gen_otp):
            user.update(is_verified=True)
            return Response({"msg":"email is verified"})
        return Response({"msg":"you have entered wrong otp"}) # raise error ok 


# forgot password
class ResetPassword(APIView):
    gen_otp = random.randint(100000,999999)
    user = User()
    def get(self,request):
        user_email = request.data["email"]
        self.user = User.objects.get(email=user_email)
        email = self.user.email
        if user_email == email:
            return Response({"msg":"email has been sent"})
        return Response({"msg":"email is failed to send"})

    def post(self,request):
        data = request.data
        otp = data["otp"]
        password = data["password"]
        password_confirm = data["password_confirm"]
        
        if str(otp) == str(self.gen_otp):
            if password == password_confirm:
                self.user.set_password(password)
                return Response({"msg":"password is set sucessfully"})
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
            return Response({"msg":"msg has been sent"})
        return Response({"msg":"msg is failed to send"})

    def post(self,request):
        data = request.data
        otp = data["otp"]
        password = data["password"]
        password_confirm = data["password_confirm"]
        
        if str(otp) == str(self.gen_otp):
            if password == password_confirm:
                self.user.set_password(password)
                return Response({"msg":"password is set sucessfully"})
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
            return Response({"msg":"mobile is verified"})
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
