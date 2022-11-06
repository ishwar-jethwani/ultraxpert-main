from django.urls import path
from .views import *

urlpatterns = [
    path("",AboutUsListAPI.as_view(),name="about"),
    path("about/",AboutUsCreateAPI.as_view(),name="about_create"),
    path("banner/",BannerListAPI.as_view(),name="banner"),
    path("banner_create/",BannerCreateAPI.as_view(),name="banner_create"),
    path("banner_read/<str:pk>/",BannerReadAPI.as_view(),name="banner_read"),
    path("contact/",SupportQueryAPI.as_view(),name="contact"),
    path("blog/",BlogListAPI.as_view(),name="blog"),
    path("blog_create/",BlogCreateAPI.as_view(),name="blog_create"),
    path("blog/<str:pk>/",BlogReadAPI.as_view(),name="blog_read"),
]