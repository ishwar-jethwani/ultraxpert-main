from django.shortcuts import render,redirect
import os
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from UltraExperts.constants import VIDEOSDK_API_KEY
from meet.models import Meeting
from meet.serializers import MeetingSerializer
from user.models import User,Services,Profile, UserPlans
from rest_framework.response import Response
from UltraExperts.settings import BASE_URL
from rest_framework import status
from events.models import EventScheduleTime




class MeetingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        service_id = request.data["service_id"]
        event_id = request.data["slot_id"]
        expert_id = request.data["expert_id"]
        consumer = Profile.objects.get(profile=user)
        expert = Profile.objects.get(profile__user_id=expert_id)
        service = Services.objects.get(service_id=service_id)
        event = EventScheduleTime.objects.get(id=event_id)
        title = service.service_name
        meet = Meeting.objects.create(
            user = consumer.profile,
            service_name = title,
            service = service,
            expert = expert,
            event = event
        )
        if meet:
            meeting_id = meet.meeting_id
            serialize = MeetingSerializer(meet)
            get_meet(self.request,meeting_id)
            return Response({"url":f'{BASE_URL}/meet/{meeting_id}/',"meet_data":serialize.data},status=status.HTTP_200_OK)
        else:
            return Response({"res":0,"msg":"you dont have meeting"},status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        meetings = Meeting.objects.filter(user=user)
        serialize = MeetingSerializer(meetings,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    
class ExpertMeeting(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        if user.is_expert == True:
            meetings = Meeting.objects.filter(expert__profile=user)
            serialize = MeetingSerializer(meetings)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        return Response({"msg":"somthing went worng"},status=status.HTTP_400_BAD_REQUEST)





def get_meet(request,meeting_id):
    data = Meeting.objects.get(meeting_id=meeting_id)
    title = data.service_name
    user = request.user
    try:
        consumer = Profile.objects.get(profile=user)
        name = "".join(f'{consumer.first_name} {consumer.last_name}')
    except:
        return redirect("login")
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