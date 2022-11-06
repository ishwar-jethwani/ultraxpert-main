from django.urls import path
from .views import *



urlpatterns = [
    path("",Home_View.as_view(),name="home"),
    path("experts/",Expert_View.as_view(),name="expert"),
    path("expert/<user_id>/",ExpertDetailView.as_view(),name="user_detail"),
    path("update/<str:user_id>/",UserUpdateAPI.as_view(),name="user_update"),
    path("profile/",Profile_View.as_view(),name="profile"),
    path("category-select/",CategoryAPIView.as_view(),name="category"),
    path("category-operations/<str:pk>/",CategoryRetriveAPIView.as_view(),name="category-operations"),
    path("service_create/",ServiceCreate.as_view(),name="service_create"),
    path("bank_detail_create/",BankDetailCreate.as_view(),name="bank_detail_create"),
    path("bank_read/",BankDetailRead.as_view(),name="bank_read"),
    path("services/",ServiceList.as_view(),name="services"),
    path("autocomplete/",AutoCompleteAPIView.as_view(),name="auto_complete"),
    path("service_detail/<service_id>/",ServiceDetail.as_view(),name="services_detail"),
    path("user_plan/",UserPlanAPIView.as_view(),name="user_plan"),
    path("user_plan_selection/",UserPlanSelect.as_view(),name="user_plan_selection"),
    path("service_update/<service_id>/",ServiceUpdate.as_view(),name="service-update"),
    path("service_delete/<service_id>/",ServiceDelete.as_view(),name="service-delete"),
    path("delete/",UserDelete.as_view(),name="delete"),
    path("comment/<str:service_id>/",CommentAPIView.as_view(),name="comment"),
    path("test_question/",UserTestAPI.as_view(),name="test_api"),
]