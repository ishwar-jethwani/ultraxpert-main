from django.db.models import query
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
from rest_framework.pagination import LimitOffsetPagination
from elasticsearch_dsl import Q
import abc
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





class ElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = ProfileSerializer
    document_class = ExpertsDocument

    @abc.abstractmethod
    def generate_q_expression(self, query):
        result = Q('multi_match',
                query=query,
                fields=['title'],
                fuzziness='auto'
            )
        return result


    def get(self, request):
        query = request.GET.get("search")
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(e, status=500)