from django.urls import path
from .views import *



urlpatterns = [
    path("rating/<user_id>/",RatingView.as_view(),name="rating"),
    path("book_service/<str:service_id>/",Place_Order.as_view(),name="order_place"),
    path("order_history/",OrderHistory.as_view(),name="order_history"),
    path("send_request/",SendProjectRequest.as_view(),name="send_request"),
    path("accept_request/<str:request_id>/",AcceptAndRejectProjectRequest.as_view(),name="accept_request"),
    path("order_confirm/<str:order_id>/",PaymentConfirmationApiView.as_view(),name="order_confirm"),
    path("order_status/<str:order_id>/",OrderStatusUpdateApiView.as_view(),name="order_status"),
    path("get_subscreption/",SubscriptionView.as_view(),name="subscreption"),
    path("your_orders/",ExpertGotOrder.as_view(),name="your_orders"),
    path("transaction/",Transaction.as_view(),name="transaction"),
    path("subs_status_update/",SubscriptonStatusUpdateApiView.as_view(),name="subs_status_update"),
    path("rated/",RatingDone.as_view(),name="rated")


]
