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

BASE_URL = os.environ["BASE_URL"]
    


class MeetingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        consumer = Profile.objects.get(profile=user)
        name = "".join(f'{consumer.first_name} {consumer.last_name}')
        if consumer.profile.is_expert==True:
            title = Services.objects.get(user=consumer.profile).service_name
            meet = Meeting.objects.create(
                expert = consumer.profile,
                service_name = title
            )
            if meet:
                serialize = MeetingSerializer(meet)
                meeting_id = meet.meeting_id
                meeting_space = get_meet(self.request,meeting_id,name,title)
                return Response({"url":f'{BASE_URL}/{meeting_id}/'})

def get_meet(request,meeting_id,name,title):
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