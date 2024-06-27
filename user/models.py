from typing import Iterable, Optional
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.base_user import BaseUserManager

from utils.custommanagers import ActiveUsersManager
from utils.constraint_fields import ContentTypeRestrictedFileField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier.
    """
    def create_user(self, email, password=None, ip_address=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        user = self.model(email=email, **extra_fields)
       
        if password:
            user.set_password(password)
       
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password. (email only for superusers)
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    """
        user modal to create takes, email and password for validation. 
        upload dashboard, avatar etc.

    Raises:
        ValidationError: 
    """

    name = models.CharField(null=True, blank=False, max_length=30)
    email = models.EmailField(unique=True, null=False, blank=False) # used only for staff/admin users

    dp = ContentTypeRestrictedFileField(upload_to='dp/', content_types=['image/png', 'image/jpeg'], 
                                        max_upload_size=5242880,  null=True, blank=True) # display profile

    ip_address = models.GenericIPAddressField(null=True, blank=True) # the ip is stored to prevent attacks on server

    is_admin = models.BooleanField(default=False) # just an indicator
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    date_joined = models.DateTimeField(default=timezone.now) # you can also use auto_add_now=True

    objects = CustomUserManager()
    activeusers_manager = ActiveUsersManager()


    USERNAME_FIELD = 'email' 

    def __str__(self):
        return f'{self.email}'
    
    def clean(self) -> None:

        cleaned = super().clean()

        return cleaned

    def save(self, *args, **kwargs):
        # only a staff can become an admin, if not staff, then not an admin
        if self.is_admin:
            self.is_staff = True

        if self.is_staff == False:
            self.is_admin = False

        if self.is_superuser == True:
            self.is_staff = True
            self.is_admin = True
        
        super().save(*args, **kwargs)


