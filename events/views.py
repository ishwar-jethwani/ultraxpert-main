from django.utils import translation
from rest_framework import status
from rest_framework import generics
from user.models import Services
from events.models import Event
from django.shortcuts import render
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView
from .constant import *
from enum import Enum
import requests
import datetime
from datetime import timedelta
import base64
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from gcsa.google_calendar import GoogleCalendar
from beautiful_date import day,weeks,months
from gcsa.reminders import EmailReminder, PopupReminder
import urllib.parse as urlparse
from urllib.parse import parse_qs
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from activity.models import Order,Subscriptions
import json
import webbrowser
from activity.serializers import *


# def base64_encode(message):
#     message_bytes = message.encode('ascii')
#     base64_bytes = base64.b64encode(message_bytes)
#     base64_message = base64_bytes.decode('ascii')
#     return base64_message


# class GoogleCalaenderAuthorizationAPIView(APIView):
#     def __init__(self):
#         self.service_account_email = CLIENT_SERVICE_ACCOUNT_EMAIL
#         self.SCOPES = [GOOGLE_CALENDER_BASE_URL]
#         credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE)
#         self.scoped_credentials = credentials.with_scopes(self.SCOPES)

    
#     def build_service(self):
#         service = build("calendar", "v3", credentials=self.scoped_credentials)
#         return service
    
#     def get(self,request,service_id):
#         users = User.objects.filter(is_expert=True)
#         events = list()
#         for user in users:
#             queryset = EventScheduleTime.objects.filter(schedule__event__expert=user)
#             service_event = queryset.filter(schedule__event__releted_service__service_id=service_id)
#             serialize = EventReadSerializer(service_event,many=True)
#             events.append(serialize.data)
#         return Response({"events":events})

        
#     def post(self,request,service_id):
#         service = self.build_service()
#         queryset = EventScheduleTime.objects.filter(schedule__event__releted_service__service_id=service_id)
#         serialize = EventReadSerializer(queryset,many=True)
#         data = json.dumps(serialize.data)
#         events = json.loads(data)
#         for schedule in events:
#             event_model_data = Event.objects.get(event_id=schedule["schedule"]["event"]["event_id"])
#             if event_model_data.notify_before_time == "5 Minutes":
#                 event_model_data.notify_before_time = 5
#             elif event_model_data.notify_before_time == "10 Minutes":
#                 event_model_data.notify_before_time = 10
#             elif event_model_data.notify_before_time == "15 Minutes":
#                 event_model_data.notify_before_time = 15
#             elif event_model_data.notify_before_time == "30 Minutes":
#                 event_model_data.notify_before_time = 30
#             elif event_model_data.notify_before_time == "1 hour":
#                 event_model_data.notify_before_time = 60
#             else:
#                 event_model_data.notify_before_time = 0

#             if event_model_data.notify_after_time == "5 Minutes":
#                 event_model_data.notify_after_time = 5
#             elif event_model_data.notify_after_time == "10 Minutes":
#                 event_model_data.notify_after_time = 10
#             elif event_model_data.notify_after_time == "15 Minutes":
#                 event_model_data.notify_after_time = 15
#             elif event_model_data.notify_after_time == "30 Minutes":
#                 event_model_data.notify_after_time = 30
#             elif event_model_data.notify_after_time == "1 hour":
#                 event_model_data.notify_after_time = 60
#             else:
#                 event_model_data.notify_after_time = 0
            
#             start_time = schedule["start_time"]
#             end_time = schedule["end_time"]
            
            

#             try:
#                 event = {
#                             'summary': schedule["schedule"]["event"]["event_name"],
#                             'description': schedule["schedule"]["event"]["discription"],
#                             'start': {
#                                 'dateTime': schedule["start_time"],
#                                 'timeZone': schedule["timezone"],
#                             },
#                             'end': {
#                                 'dateTime': schedule["end_time"],
#                                 'timeZone': schedule["timezone"],
#                             },
#                             'recurrence': [
#                                 'RRULE:FREQ=WEEKLY'
#                             ],

#                             'reminders': {
#                                 'useDefault': False,
#                                 'overrides': [
#                                 {'method': 'email', 'minutes': event_model_data.notify_before_time},
#                                 {'method': 'popup', 'minutes': event_model_data.notify_after_time},
#                                 ],
#                             },
#                         }

#                 event = service.events().insert(calendarId='primary', body=event).execute()
#                 return Response({"event":event})
#             except Exception as e:
#                 raise ValidationError(detail=e,code=400)

     
class EventCreateAPIView(CreateAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EventCreateSerializer

class GetEventAPIView(APIView):
    pass









            







        

        

      
        




