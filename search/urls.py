from django.urls import path
from .views import *


urlpatterns = [
    path("search_expert/",ExpertSearchView.as_view(),name="search"),
    path("search_services/",ExpertServicesSearchView.as_view(),name="search_services"),
    path("search_keyword/",SearchView.as_view(),name="search"),
    path("",ElasticSearchAPIViewSet.as_view({'get': 'list'}),name="es_search")


]