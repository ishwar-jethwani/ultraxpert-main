from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .constant import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.generics import CreateAPIView
from activity.serializers import *
from .models import *
from collections import defaultdict


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
    def get(self,request,service_id):
        event = Event.objects.filter(releted_service__service_id=service_id)
        list_of_event = event.values_list("event_id",flat=True)
        event = EventSchedule.objects.filter(event__event_id__in=list(list_of_event))
        if request.GET.get("date") is not None:
            event_day = event.filter(day=request.GET.get("date"))
        else:
            event_day = event
        list_of_event_schedule =  event_day.values_list("pk",flat=True)
        slots = EventScheduleTime.objects.filter(schedule__pk__in=list(list_of_event_schedule))
        slots = slots.filter(booked=False)
        serialize = EventReadSerializer(slots,many=True)
        result = defaultdict(list)
        for i in range(len(serialize.data)):
            current = serialize.data[i]
            current = dict(current)
            print(current)
            for key,value in current.items():
                if type(current[key])==list:
                    for j in range(len(value)):
                        result[key].append(value[j])

        if serialize:
            return Response(serialize.data,status=status.HTTP_200_OK)

class BookedStatusChangeAPI(APIView):
    def post(self,request):
        slot_id = request.data["slot_id"]
        payment_id = request.data["payment_id"]
        payment = PaymentStatus.objects.filter(payment_id=payment_id)
        if payment.first().status=="authorized" or payment.first().status=="captured":
            slot = EventScheduleTime.objects.filter(id=slot_id)
            slot.update(booked=True)
            return Response({"msg":"you have successfully booked this time slot"},status=status.HTTP_200_OK)
        return Response({"msg":"not booked"},status=status.HTTP_400_BAD_REQUEST)

            
        

        



        



        




    









            







        

        

      
        




