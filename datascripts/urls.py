from django.urls import path,include
from .views import *

urlpatterns = [
        path("cat_data/",Category_Create.as_view(),name="cat_data"),
        # path("",TestCreateUserData.as_view(),name="user_data"),
        #path("",TestServiceCreate.as_view(),name="service_create")
        path("",TestQuestion.as_view(),name="test_data")

]
