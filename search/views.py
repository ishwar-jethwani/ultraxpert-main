from multiprocessing import Event
from user.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import filters
from user.models import *
from django.db.models.query_utils import Q
from django.core.paginator import Paginator

class ExpertSearchView(generics.ListAPIView):
    """List APIView For Filtering Expert"""
    queryset = Profile.objects.filter(profile__is_expert=True)
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["first_name","last_name","profile__username","profile__email"]


class ExpertServicesSearchView(generics.ListAPIView):
    """List APIView For Filtering Expert Depending On Service"""
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["service_name"]

class CategorySearchView(APIView):
    """APIView For Searching Category"""
    def get(self,request):
        data = request.GET.get("search")
        category = Category.objects.get(name=data)
        related_service = Services.objects.filter(category=category)
        serialize = ServiceShowSerializer(related_service,many=True)
        if serialize:
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response({"msg":"we could not find any profile releted to this category"})


class SearchAPIView(APIView):
    """API View For Search"""
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




# class ES_ExpertSearch(APIView):
#     def get(self,request):
#         search = request.GET.get("search")
#         try:
#             expert = ExpertsDocument.search().query("query_string", query=search)
#             serialize = ExpertDocumentSerializer(expert,many=True)
#             return Response(data=serialize.data,status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response({"status":"ok","data":"Not Found!"})



# class ES_ServiceSearch(APIView):
#     def get(self,request):
#         search = request.GET.get("search")
#         try:
#             service = ServiceDocument.search().query("query_string", query=search)
#             serialize = ServiceDocumentSerializer(service,many=True)
#             return Response(data=serialize.data,status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response({"status":"ok","data":"Not Found!"})

class ES_ExpertSearch(APIView):
        """APIView For Searching Expert"""
        def get(self,request):
            page_number= 1
            request_data = request.GET
            if "search" in request_data:
                search = request_data.get("search")
                search_1 = search.split(" ")
                search = search_1[0]
            if "page" in request_data:
                page_number = request_data.get("page")
            try:
                experts = Profile.objects.filter(Q(first_name__icontains=search)|Q(last_name__icontains=search)|Q(categories__name__icontains=search)|Q(description__icontains=search))
                experts = Paginator(experts,30)
                experts = experts.page(int(page_number))
                serialize = ExpertSearchSerializer(experts,many=True)
                return Response(data=serialize.data,status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"status":"ok","data":"Not Found!"})


class ES_ServiceSearch(APIView):
    """APIView For Searching Expert According To Service  """
    def get(self,request):
        search = request.GET.get("search")
        page_number= 1
        if "page" in request.GET:
            page_number = request.GET["page"]
        try:
            service = Services.objects.filter(Q(service_name__icontains=search)|Q(category__name__icontains=search)|Q(description__icontains=search))
            service = Paginator(service,30)
            service = service.page(int(page_number))
            serialize = ServiceSearchSerializer(service,many=True)
            return Response(data=serialize.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status":"ok","data":"Not Found!"})

class TimeSearch(APIView):
    """APIView For Search Time"""
    def get(self,request):
        data = request.GET
        if "date" in data:
            pass
        else:
            pass
