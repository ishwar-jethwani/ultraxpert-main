from django.contrib.auth.backends import ModelBackend
from user.models import User
class MobileAuthenticationBackend(ModelBackend):
    """Authentication Through Mobile And Password"""
    def authenticate(self, request, **kwargs):
        mobile = kwargs["mobile"]
        password = kwargs["password"]
        try:
            user = User.objects.get(mobile=mobile)
            if user.check_password(password) is True:
                return user
        except user.DoseNotExist:
            return None