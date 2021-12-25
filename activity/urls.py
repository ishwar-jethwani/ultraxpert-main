from os import name
from django.urls import path,include
from .views import *



urlpatterns = [
    path("rating/<str:pk>/",RatingView.as_view(),name="rating"),
    path("book_service/<str:service_id>/",Place_Order.as_view(),name="order_place"),
    path("order_history/",OrderHistory.as_view(),name="order_history"),
    path("search_expert/",ExpertSearchView.as_view(),name="search"),
    path("search_services/",ExpertServicesSearchView.as_view(),name="search_services"),
    path("user/<str:pk>/",ExpertDetailView.as_view(),name="user_detail"),
    path("send_request/",SendProjectRequest.as_view(),name="send_request"),
    path("accept_request/<str:request_id>/",AcceptAndRejectProjectRequest.as_view(),name="accept_request"),
    path("order_confirm/<str:order_id>/",PaymentConfirmationApiView.as_view(),name="order_confirm"),
    path("order_status/<str:order_id>/",OrderStatusUpdateApiView.as_view(),name="order_status"),
    path("get_subscreption/",SubscriptionView.as_view(),name="subscreption"),
    path("your_orders/",ExpertGotOrder.as_view(),name="your_orders"),
    path("search/",SearchView.as_view(),name="search"),

]