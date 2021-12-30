from user.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import json
from rest_framework import filters
from user.models import *
from rest_framework import permissions


class ExpertSearchView(generics.ListAPIView):
    queryset = Profile.objects.filter(profile__is_expert = True)
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["first_name","last_name","profile__username","profile__email"]


class ExpertServicesSearchView(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["service_name"]

class SearchView(APIView):
    def get(self,request):
        data = request.data["serach"]
        try:
            keyword = Keywords.objects.get(name=data)
            related_expert = Profile.objects.filter(keywords=keyword)
        except:
            category = Category.objects.get(name=data)
            related_expert = Profile.objects.filter(categories=category)
        serialize = ProfileSerializer(related_expert,many=True)
        if serialize:
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response({"msg":"we could not find any profile releted to this keyword or category"})
