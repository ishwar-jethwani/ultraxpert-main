from django.urls import path,include
from .views import *

urlpattern = [
    path("search_expert/",ExpertSearchView.as_view(),name="search"),
    path("search_services/",ExpertServicesSearchView.as_view(),name="search_services"),
    path("search_keyword/",SearchView.as_view(),name="search"),

]