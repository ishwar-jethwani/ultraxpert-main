from django.urls import path,include
from googleapiclient.model import Model
from .views import *



urlpatterns = [
    path("",Expert_View.as_view(),name="home"),
    path("expert/<str:pk>/",ExpertDetailView.as_view(),name="user_detail"),
    path("update/<str:user_id>/",UserUpdateAPI.as_view(),name="user_update"),
    path("profile/<str:pk>/",Profile_View.as_view(),name="profile"),
    path("category-select/",CategoryAPIView.as_view(),name="category"),
    path("category-operations/<str:pk>/",CategoryRetriveAPIView.as_view(),name="category-operations"),
    path("social_link/",SocialMedia_view.as_view(),name="sociallink"),
    path("user_social_links/<str:user_id>/",SocialMediaLinks.as_view(),name="social_handles"),
    path("service_create/",ServiceCreate.as_view(),name="service_create"),
    path("services/",ServiceList.as_view(),name="services"),
    path("autocomplete/",AutoCompleteAPIView.as_view(),name="auto_complete"),
    path("service_detail/<service_id>/",ServiceDetail.as_view(),name="services_detail"),
    path("user_plan/",UserPlanAPIView.as_view(),name="user_plan"),
    path("user_plan_selection/",UserPlanSelect.as_view(),name="user_plan_selection"),
    path("service/read-update-delete/<str:pk>/",ServiceRetriveUpdateDelete.as_view(),name="service-read-update-delete"),
    path("delete/",UserDelete.as_view(),name="delete"),
    path("comment/",CommentAPIView.as_view(),name="comment"),
    

]