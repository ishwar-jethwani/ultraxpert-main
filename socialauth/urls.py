from django.urls import path

from .views import GoogleSocialAuthView,FaceBookLogin

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    path("facebook/",FaceBookLogin.as_view(),name="fb_login")
    ]