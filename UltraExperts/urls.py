from django.contrib import admin
from django.urls import path,include
from allauth.account.views import confirm_email
from rest_auth.views import PasswordResetConfirmView
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from dj_rest_auth.views import PasswordChangeView,LogoutView
from django.conf import settings
from dj_rest_auth import registration


admin.site.site_header = settings.ADMIN_SITE_HEADER

from .views import *
from . import views


schema_view = get_schema_view(
   openapi.Info(
      title="UltraExperts API",
      default_version='Beta',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Security

urlpatterns = [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path("privacy/",privacy,name="privacy"),
    
]

#Authentication

urlpatterns+=[
   path("register/",include('dj_rest_auth.registration.urls')),
   path("login/",CustomLoginView.as_view(),name="login"),
   path("logout/",LogoutView.as_view(),name="logout"),
   path("reset/",ResetPassword.as_view(),name="reset_password"),
   path("change/",PasswordChangeView.as_view(),name="change_password"),
   path("account/",include("allauth.urls")),
   path('auth/',include('rest_framework_social_oauth2.urls')),
   path("verification/",UserEmailVerification.as_view(),name="verification"),
   path("file/upload/",FileUploadView.as_view(),name="upload"),
   path("mobile_reset_password/",MobileResetPassword.as_view(),name="mobile_password_reset"),
   path("mobile_verification/",MobileVerificationApi.as_view(),name="mobile_verification"),
   path("mobile_register/",MobileUserCreate.as_view(),name="mobile_register"),
   path("mobile_login/",MobileLogin.as_view(),name="mobile_login"),


]
urlpatterns+=[
      path("facebook/", FacebookLogin.as_view(), name='fb_login'),
      # path("google/",GoogleLogin.as_view(),name="google_login")
]

# Sysytem Application
urlpatterns+=[
   path("user/",include("user.urls")),
   path("activity/",include("activity.urls")),
   path("chat/",include("chat.urls")),
   path("events/",include("events.urls")),
   path("payments/",include("payment.urls")),
   path("meet/",include('meet.urls')),
   path("search/",include("search.urls"))

]

