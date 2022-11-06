from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifiers for authentication instead of usernames."""
    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        #user = self.model._meta.get_field('username')._unique = False
        user.set_password(password)
        user.save()
        return user

    def create_mobile_user(self,mobile,password,username,**extra_fields):
        """Create And Saving a User Using mobile"""
        if not mobile:
            raise ValueError('The given phone must be set')
        self.mobile = mobile
        user = self.model(mobile=mobile,username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_expert(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_expert', True)


        if extra_fields.get('is_expert') is not True:
            raise ValueError(_('Expert must have is_staff=True.'))
        return self.create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)