from django.apps import AppConfig
from django.db.models.signals import post_save

# from UltraExperts.views import User_Type
class UserConfig(AppConfig):
    """App Config For User"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from user import signals  







