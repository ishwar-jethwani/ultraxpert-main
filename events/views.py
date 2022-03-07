from faulthandler import disable
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from meet.models import Meeting
from .constant import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.generics import CreateAPIView
from activity.serializers import *
from .models import *
from collections import defaultdict
from datetime import datetime,date


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


class GlobalCheckAPI(APIView):
    def post(self,request):
        expert_id = request.data["expert_id"]
        slot_id = request.data["slot_id"]
        user = User.objects.get(user_id=expert_id)
        services = Services.objects.filter(user=user)
        sevices_list = services.values_list("id",flat=True)
        events_slots = EventScheduleTime.objects.filter(schedule__event__releted_service__in=list(sevices_list))
        booked_slot = events_slots.get(pk=slot_id)
        booked_start_time = booked_slot.start_time
        booked_end_time = booked_slot.end_time
        booked_date = booked_slot.schedule.day
        booked_start_date_time_obj = datetime.strptime(booked_date+"/"+booked_start_time,"%d/%m/%Y/%H:%M")
        booked_end_date_time_obj = datetime.strptime(booked_date+"/"+booked_end_time,"%d/%m/%Y/%H:%M")
        for slot in events_slots:
            slot_start_date_time = datetime.strptime(slot.schedule.day+"/"+slot.start_time,"%d/%m/%Y/%H:%M")
            slot_end_date_time =  datetime.strptime(slot.schedule.day+"/"+slot.end_time,"%d/%m/%Y/%H:%M")
            if booked_start_date_time_obj+timedelta(minutes=15)<=slot_start_date_time and slot_end_date_time<=booked_end_date_time_obj+timedelta(minutes=15):
                slot.disable = True
                slot.save()    
        return Response(data={"msg":"sucessfully Updated"},status=status.HTTP_200_OK)


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
        current_time = datetime.now()
        slots = slots.filter(booked=False,disable=False)
        time_slots = list()
        for slot in slots:
            date_time_obj = datetime.strptime(slot.schedule.day+"/"+slot.start_time,"%d/%m/%Y/%H:%M")
            if current_time<=date_time_obj:
                time_slots.append(slot)
        serialize = EventReadSerializer(time_slots,many=True)
        result = defaultdict(list)
        slot_dict =  defaultdict(list)
        for i in range(len(serialize.data)):
            current = serialize.data[i]
            for main_key,val in current.items():
                if main_key == "slots":
                    for key, value in current["slots"].items():
                        for j in range(len(value)):
                            slot_dict[key].append(value[j])
                    result.update({"slots":slot_dict})
                else:
                    result.update({main_key:val})
        if serialize:
            return Response(result,status=status.HTTP_200_OK)

class BookedStatusChangeAPI(APIView):
    def post(self,request):
        slot_id = request.data["slot_id"]
        payment_id = request.data["payment_id"]
        payment = PaymentStatus.objects.filter(payment_id=payment_id)
        if payment.first().status=="authorized" or payment.first().status=="captured":
            slot = EventScheduleTime.objects.filter(id=slot_id)
            slot.update(booked=True)
            slot_ids = slot.values_list("id",flat=True)
            orders = Order.objects.filter(slot__id__in=list(slot_ids))
            for order in orders:
                html1 = get_template("service_confirmation.html")
                html2 = get_template("service_confirmation_paid.html")
                html1 = html1.render({"user_id":order.user.user_id,"service_name":order.service_obj.service_name,"start_time":order.slot.start_time,"end_time":order.slot.end_time,"duration":order.slot.duration,"amount":order.price,"date":order.slot.schedule.day})
                html2 = html2.render({"service_name":order.service_obj.service_name,"start_time":order.slot.start_time,"end_time":order.slot.end_time,"duration":order.slot.duration,"amount":order.price,"date":order.slot.schedule.day})
                send_mail(
                        from_email = None,
                        recipient_list = [order.order_on.email],
                        subject ="Service Booked",
                        html_message = html1,
                        message = "Service Booked"
                    
                )
                send_mail(
                        from_email = None,
                        recipient_list = [order.user.email],
                        subject ="Service Booked",
                        html_message = html2,
                        message = "Service Booked"
                    
                )
                return Response({"msg":"you have successfully booked this time slot"},status=status.HTTP_200_OK)
        return Response({"msg":"not booked"},status=status.HTTP_400_BAD_REQUEST)

            
        

        



        



        




    









            







        

        

      
        




