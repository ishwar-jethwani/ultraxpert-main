from rest_framework import serializers
from .models import *





class EventReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventScheduleTime
        fields = "__all__"
        depth = 2


class EventScheduleTimeCreateSerializer(serializers.ModelSerializer):
    """
    Helper Serializer for Creating an event
    """
    class Meta:
        model = EventScheduleTime
        fields = ['start_time', 'end_time','timezone','booked']


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

