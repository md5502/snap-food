from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(BaseModel):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_number = models.CharField(max_length=16)
    profile_image = models.ImageField(default="uploads/profile_images/default.jpg", upload_to="uploads/profile_images")

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}-{self.email}"
