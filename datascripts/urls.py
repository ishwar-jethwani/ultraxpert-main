from django.urls import path,include
from .views import *

urlpatterns = [
        path("cat_data/",Category_Create.as_view(),name="cat_data"),
        path("",CreateUserData.as_view(),name="user_data"),

]
