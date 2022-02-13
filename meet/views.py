import os
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from UltraExperts.constants import VIDEOSDK_API_KEY
from meet.models import Meeting, MeetingTypeCount
from meet.serializers import MeetingSerializer,MeetingContainerSerializer
from payment.models import PaymentStatus
from user.models import User,Services,Profile, UserPlans
from rest_framework.response import Response
from UltraExperts.settings import BASE_URL
from rest_framework import status
from events.models import EventScheduleTime
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

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
            return Response({"meet_data":serialize.data},status=status.HTTP_200_OK)
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
        print(user)
        if user.is_expert == True:
            meetings = Meeting.objects.filter(expert__profile=user)
            serialize = MeetingSerializer(meetings,many=True)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        return Response({"msg":"somthing went worng"},status=status.HTTP_400_BAD_REQUEST)


class MeetingValidation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,meeting_id):
        user = request.user
        try:
            meeting = Meeting.objects.get(meeting_id=meeting_id)
            print(meeting)
            if meeting.expert.profile==user:
                token = RefreshToken.for_user(user)
                access_token = token.access_token
                access_token.set_exp(lifetime=timedelta(minutes=meeting.event.duration))
                return Response({"msg":"Success","token":str(token.access_token)},status=status.HTTP_200_OK)
            elif meeting.user==user:
                token = RefreshToken.for_user(user)
                access_token = token.access_token
                access_token.set_exp(lifetime=timedelta(minutes=meeting.event.duration))
                return Response({"msg":"Success","token":str(token.access_token)},status=status.HTTP_200_OK)
            else:
                return Response({"msg":"Bad Request"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"msg":"Meeting is not defined"},status=status.HTTP_404_NOT_FOUND)


class MeetingContainer(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user  
        meeting_buyed = MeetingTypeCount.objects.create(user=user,meet_45=0,meet_30=3,meet_60=0) 
        serilize = MeetingContainerSerializer(meeting_buyed)
        if serilize.is_valid():
            return Response(data=serilize.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data={"msg":"Somthing Went Wrong"},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        user = request.user
        meeting_container = MeetingTypeCount.objects.get(user=user)
        serilize = MeetingContainerSerializer(meeting_container)
        if serilize.is_valid():
            return Response(data=serilize.data,status=status.HTTP_200_OK)
        else:
            return Response(data={"msg":"Somthing Went Wrong"},status=status.HTTP_400_BAD_REQUEST)
        
    def update(self,request):
        user = request.user
        meeting_plan = int(request.data["select_plan"])
        meeting = request.data["meetings"]
        payment_id = request.data["payment_id"]
        payment = PaymentStatus.objects.filter(payment_id=payment_id)
        if payment.exists():
            meeting_container = MeetingTypeCount.objects.get(user=user)
            if meeting_plan ==1:
                no_of_meeting = meeting_container.meet_60
                meeting_container.meet_60=no_of_meeting+meeting
                meeting_container.save(updated_fields=["meet_60"])
            elif meeting_plan ==2:
                no_of_meeting = meeting_container.meet_45
                meeting_container.meet_45=no_of_meeting+meeting
                meeting_container.save(updated_fields=["meet_45"])
            elif meeting_plan ==3:
                no_of_meeting = meeting_container.meet_30
                meeting_container.meet_30=no_of_meeting+meeting
                meeting_container.save(updated_fields=["meet_30"])
            serialize = MeetingContainerSerializer(meeting_container)
            if serialize.is_valid():
                return Response(data=serialize.data,status=status.HTTP_200_OK)
            else:
                return Response(data={"msg":"data is not valid"},status=status.HTTP_200_OK)
        else:
            return Response(data={"msg":"somthing went wrong"},status=status.HTTP_400_BAD_REQUEST)

        
            



        



        





    



# def get_meet(request,meeting_id):
#     data = Meeting.objects.get(meeting_id=meeting_id)
#     title = data.service_name
#     user = request.user
#     try:
#         consumer = Profile.objects.get(profile=user)
#         name = "".join(f'{consumer.first_name} {consumer.last_name}')
#     except:
#         return redirect("login")
#     key = ""
#     try:
#         key = os.environ["API_KEY"]
#     except KeyError:
#         key = VIDEOSDK_API_KEY
    
#     context = {
#         "API_KEY":str(key),
#         "name":name,
#         "meeting_id":str(meeting_id),
#         "title":str(title)
#     }
#     return render(request,"meet.html",context)