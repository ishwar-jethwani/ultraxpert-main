from django.urls import path,include
from .views import *

urlpatterns = [
    path('', ChatSessionView.as_view()),
    path('<uri>/',ChatSessionView.as_view()),
    path('<uri>/messages/',ChatSessionMessageView.as_view()),
]