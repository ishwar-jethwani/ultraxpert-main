from django.urls import path
from .views import *


urlpatterns = [
    path("search_expert/",ExpertSearchView.as_view(),name="search"),
    path("search_services/",ExpertServicesSearchView.as_view(),name="search_services"),
    path("search_category/",CategorySearchView.as_view(),name="search"),
    path("es_expert/",ES_ExpertSearch.as_view(),name="es_expert"),
    path("es_service/",ES_ServiceSearch.as_view(),name="es_service"),
    path("search_save/",SearchAPIView.as_view(),name="search_save")

]