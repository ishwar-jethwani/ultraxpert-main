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
from datetime import datetime, timedelta

class MeetingAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        service_id = request.data["service_id"]
        event_id = request.data["slot_id"]
        expert_id = request.data["expert_id"]
        expert = Profile.objects.get(profile__user_id=expert_id)
        service = Services.objects.get(service_id=service_id)
        event = EventScheduleTime.objects.get(id=event_id)
        title = service.service_name
        meet = Meeting.objects.create(
            user = user,
            service_name = title,
            service = service,
            expert = expert,
            event = event
        )
        if meet:
            meetings = MeetingTypeCount.objects.get(user=meet.expert.profile)
            if meet.event.duration==30:
                meeting_30=meetings.meet_30
                meetings.meet_30 = meeting_30-1
                meetings.save(update_fields=["meet_30"])
            elif meet.event.duration==45:
                meeting_45=meetings.meet_45
                meetings.meet_45 = meeting_45-1
                meetings.save(update_fields=["meet_45"])
            elif meet.event.duration==60:
                meeting_60 = meetings.meet_60
                meetings.meet_60 = meeting_60-1
                meetings.save(update_fields=["meet_60"])
            serialize = MeetingSerializer(meet)
            return Response({"meet_data":serialize.data},status=status.HTTP_200_OK)
        else:
            return Response({"res":0,"msg":"you dont have meeting"},status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        meetings = Meeting.objects.filter(user=user)
        current_time = datetime.now()
        for meet in meetings:
            meet_date_start_time_obj = datetime.strptime(meet.event.schedule.day+"/"+meet.event.start_time,"%d/%m/%Y/%H:%M")
            meet_date_end_time_obj = datetime.strptime(meet.event.schedule.day+"/"+meet.event.end_time,"%d/%m/%Y/%H:%M")
            if current_time>=meet_date_start_time_obj and current_time<=meet_date_end_time_obj:
                meet.join_btn = True
            else:
                meet.join_btn = False
            meet.save(update_fields=["join_btn","rating_btn"])
        serialize = MeetingSerializer(meetings,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    
class ExpertMeeting(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        current_time = datetime.now()
        if user.is_expert == True:
            meetings = Meeting.objects.filter(expert__profile=user)
            meeting_credit = MeetingTypeCount.objects.get(user=user)
            for meet in meetings:
                meet_date_start_time_obj = datetime.strptime(meet.event.schedule.day+"/"+meet.event.start_time,"%d/%m/%Y/%H:%M")
                meet_date_end_time_obj = datetime.strptime(meet.event.schedule.day+"/"+meet.event.end_time,"%d/%m/%Y/%H:%M")
                if meet.event.duration == 30:
                    if meeting_credit.meet_30<=0:
                        meet.add_meeting_btn = True
                        meet.join_btn = False
                    else:
                        if current_time>=meet_date_start_time_obj and current_time<=meet_date_end_time_obj:
                            meet.join_btn = True
                        meet.add_meeting_btn = False
                elif meet.event.duration == 45:
                    if meeting_credit.meet_45<=0:
                        meet.add_meeting_btn = True
                        meet.join_btn = False
                    else:
                        if current_time>=meet_date_start_time_obj and current_time<=meet_date_end_time_obj:
                            meet.join_btn = True
                        meet.add_meeting_btn = False 
                elif meet.event.duration == 60:
                    if meeting_credit.meet_60<=0:
                        meet.add_meeting_btn = True
                        meet.join_btn = False
                    else:
                        if current_time>=meet_date_start_time_obj and current_time<=meet_date_end_time_obj:
                            meet.join_btn = True
                        meet.add_meeting_btn = False 
                else:
                    meet.join_btn = False
                meet.save(update_fields=["join_btn","add_meeting_btn"])
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
        if serilize:
            return Response(serilize.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"msg":"Somthing Went Wrong"},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        user = request.user
        meeting_container = MeetingTypeCount.objects.get(user=user)
        serilize = MeetingContainerSerializer(meeting_container)
        if serilize:
            return Response(serilize.data,status=status.HTTP_200_OK)
        else:
            return Response({"msg":"Somthing Went Wrong"},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
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
                meeting_container.save(update_fields=["meet_60"])
            elif meeting_plan ==2:
                no_of_meeting = meeting_container.meet_45
                meeting_container.meet_45=no_of_meeting+meeting
                meeting_container.save(update_fields=["meet_45"])
            elif meeting_plan ==3:
                no_of_meeting = meeting_container.meet_30
                meeting_container.meet_30=no_of_meeting+meeting
                meeting_container.save(update_fields=["meet_30"])
            serialize = MeetingContainerSerializer(meeting_container)
            if serialize:
                return Response(serialize.data,status=status.HTTP_200_OK)
            else:
                return Response({"msg":"data is not valid"},status=status.HTTP_200_OK)
        else:
            return Response({"msg":"somthing went wrong"},status=status.HTTP_400_BAD_REQUEST)

        
class MeetingQuikeJoin(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        meeting_id = request.data["meeting_id"]
        meet = Meeting.objects.get(meeting_id=meeting_id)
        current_time = datetime.now()
        if meet:
            meet_date_start_time_obj = datetime.strptime(meet.event.schedule.day+"/"+meet.event.start_time,"%d/%m/%Y/%H:%M")
            meet_date_end_time_obj = datetime.strptime(meet.event.schedule.day+"/"+meet.event.end_time,"%d/%m/%Y/%H:%M")
            if current_time>=meet_date_start_time_obj and current_time<=meet_date_end_time_obj:
                meet.join_btn = True
                meet.add_meeting_btn = False
                meet.save(update_fields=["join_btn","add_meeting_btn"])
                serialize = MeetingSerializer(meet)
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response(serialize.data,status=status.HTTP_400_BAD_REQUEST)


        



        



        





    



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