from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

from ..utlis import phone_regex


class CustomUserManager(BaseUserManager):
    def create_user(self, email,phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is Necessary")

        if not phone:
            raise ValueError("Phone Number is Necessary")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user(phone=phone)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone,password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True  ")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True ")

        return self.create_user(email,phone, password, **extra_fields)


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(
        validators=[
            phone_regex,
        ],
        unique=True
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone',]
