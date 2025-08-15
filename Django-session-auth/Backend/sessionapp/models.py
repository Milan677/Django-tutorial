from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.timezone import now,timedelta
from django.utils.crypto import get_random_string

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,email, name, password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Optional: You can omit this as AbstractBaseUser already has it

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]  # Fields required for createsuperuser

    def __str__(self):
        return self.email