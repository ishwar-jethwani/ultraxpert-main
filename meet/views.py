from django.shortcuts import render
import os
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from UltraExperts.constants import VIDEOSDK_API_KEY
from meet.models import Meeting
from user.models import User,Services,Profile
from django.db.models.query_utils import Q
from .serializers import MeetingSerializer
from rest_framework.response import Response


class MeetingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def meet(self,request):
        user = request.user
        consumer = Profile.objects.get(profile=user)
        name = "".join(f'{consumer.first_name} {consumer.last_name}')
        if consumer.is_expert==True:
            title = Services.objects.get(user=consumer).service_name
            meet = Meeting.objects.create(
                expert = consumer,
                service_name = title
            )
            if meet:
                serialize = MeetingSerializer(meet)
                meeting_space = self.get(self.request,meet.meeting_id,name,title)
                return meeting_space
    
    def get(request,meeting_id,name,title):
        key = ""
        try:
            key = os.environ["API_KEY"]
        except KeyError:
            key = VIDEOSDK_API_KEY
        
        context = {
            "API_KEY":str(key),
            "name":name,
            "meeting_id":str(meeting_id),
            "title":str(title)
        }
        return render(request,"meet.html",context)
