from rest_framework import serializers
from .models import *
import datetime





class EventReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventScheduleTime
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        id=instance.pk,
        event_date = instance.schedule.day
        event_start_time = instance.start_time
        event_end_time = instance.end_time
        timezone = instance.timezone
        booked = instance.booked
        event_id = instance.schedule.event.event_id
        event_name = instance.schedule.event.event_name
        discription = instance.schedule.event.discription
        notify_before = instance.schedule.event.notify_before
        notify_before_time = instance.schedule.event.notify_before_time
        notify_after = instance.schedule.event.notify_after
        notify_after_time = instance.schedule.event.notify_after_time
        date_created = datetime.datetime.strftime(instance.schedule.event.date_created,"%c")

        data_dict = {
            
            "event_id":event_id,
            "event_name":event_name,
            "description":discription,
            "notify_before":notify_before,
            "notify_before_time":notify_before_time,
            "notify_after":notify_after,
            "notify_after_time":notify_after_time,
            "date_created":date_created,
            "slots":{event_date:[{"id":int(id[0]),"start_time":event_start_time,"end_time":event_end_time,"timezone":timezone,"booked":booked}]},
            
        }
        return data_dict




class EventScheduleTimeCreateSerializer(serializers.ModelSerializer):
    """
    Helper Serializer for Creating an event
    """
    class Meta:
        model = EventScheduleTime
        fields = ['start_time','end_time','timezone','booked']


class EventScheduleCreateSerializer(serializers.ModelSerializer):
    timings = EventScheduleTimeCreateSerializer(many=True, required=False)
    class Meta:
        model = EventSchedule
        fields = ['day', 'timings']



class EventCreateSerializer(serializers.ModelSerializer):
    schedules = EventScheduleCreateSerializer(many=True, required=False)
    class Meta:
        model = Event
        fields = [
            "event_id",
            "event_name",
            "discription",
            "expert",
            "releted_service",
            "notify_before",
            "notify_before_time",
            "notify_after",
            "notify_after_time",
            "date_created",
            "date_updated",
            "schedules"
        ]

    def create(self, validated_data):
        schedules = validated_data.pop("schedules", [])
        instance = Event.objects.create(**validated_data)
        
        
        # checking the length of schedules list
        if len(schedules) > 0:
            for schedule in schedules:
                timings = schedule.pop('timings')
                schedule_instance = EventSchedule.objects.create(**schedule, event=instance)

                if len(timings) > 0:
                    for timing in timings:
                        EventScheduleTime.objects.create(**timing, schedule=schedule_instance)

        return instance

    # def update(self, validated_data):
    #     schedules = validated_data.pop("schedules", [])
    #     instance = Event.objects.create(**validated_data)
        
        
    #     # checking the length of schedules list
    #     if len(schedules) > 0:
    #         for schedule in schedules:
    #             timings = schedule.pop('timings')
    #             schedule_instance = EventSchedule.objects.(**schedule, event=instance)

    #             if len(timings) > 0:
    #                 for timing in timings:
    #                     EventScheduleTime.objects.create(**timing, schedule=schedule_instance)

    #     return instance

