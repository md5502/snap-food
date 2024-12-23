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


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="Home")
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=16)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Iran")
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ["-is_default"]

    def __str__(self):
        return f"{self.title} - {self.user.email}"



class UserProfile(BaseModel):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_number = models.CharField(max_length=16)
    profile_image = models.ImageField(default="profile_images/default.jpg", upload_to="profile_images")
    address = models.CharField
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}-{self.email}"
