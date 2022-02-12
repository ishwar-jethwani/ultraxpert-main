from user.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import filters
from user.models import *
from .documents import *

 

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

class CategorySearchView(APIView):
    def get(self,request):
        data = request.GET.get("search")
        category = Category.objects.get(name=data)
        related_service = Services.objects.filter(category=category)
        serialize = ServiceShowSerializer(related_service,many=True)
        if serialize:
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response({"msg":"we could not find any profile releted to this category"})


class SearchAPIView(APIView):
    def post(self,request):
        try:
            search = request.GET.get("search")
            data = Search(query=search)
            data.save()
        except Exception as e:
            print(e)
            return Response({"msg":"somthing went wrong","error":e},status=500)
    def get(self,request):
        data = Search.objects.all()
        serialize = SearchSerializer(data,many=True)
        search_list = list()
        for query in serialize.data:
            search_list.append(query["query"])
        search_set = set(search_list)
        return Response(data=search_set,status=status.HTTP_200_OK)




class ES_ExpertSearch(APIView):
    def get(self,request):
        search = request.GET.get("search")
        try:
            expert = ExpertsDocument.search().query("query_string", query=search)
            serialize = ExpertDocumentSerializer(expert,many=True)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status":"ok","data":"Not Found!"})



class ES_ServiceSearch(APIView):
    def get(self,request):
        search = request.GET.get("search")
        try:
            service = ServiceDocument.search().query("query_string", query=search)
            serialize = ServiceDocumentSerializer(service,many=True)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status":"ok","data":"Not Found!"})
