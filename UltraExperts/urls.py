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

from UltraExperts.settings import PLATEFORM

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
   path("login/",CustomLoginView.as_view(),name="login"),
   path("logout/",LogoutView.as_view(),name="logout"),
   path("reset/",ResetPassword.as_view(),name="reset_password"),
   path("change/",PasswordChangeView.as_view(),name="change_password"),
   path("account/", include("allauth.urls")),
   path("verification/",UserEmailVerification.as_view(),name="verification"),
   path("file/upload/",FileUploadView.as_view(),name="upload"),
   path('social/', include('rest_framework_social_oauth2.urls')),
   path("mobile_reset_password/",MobileResetPassword.as_view(),name="mobile_password_reset"),
   path("mobile_verification/",MobileVerificationApi.as_view(),name="mobile_verification"),

]

# Sysytem Application
urlpatterns+=[
   path("user/",include("user.urls")),
   path("activity/",include("activity.urls")),
   path("chat/",include("chat.urls")),
   path("events/",include("events.urls")),
   path("payments/",include("payment.urls")),
   path("socialauth/",include("socialauth.urls")),
   path('register/', include('dj_rest_auth.registration.urls')),
   path("meet/",include('meet.urls')),
   path("search/",include("search.urls"))

]
