from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from common.models import BaseModel
from users.models import CustomUser


class Restaurant(BaseModel):
    RATE_CHOSES = (
        ("1", "very bad"),
        ("2", "bad"),
        ("3", "natural"),
        ("4", "good"),
        ("5", "very good"),
    )
    name = models.CharField(max_length=120)
    logo = models.ImageField(default="restaurants/default.jpg", upload_to="restaurants")
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="restaurants")
    address = models.CharField(max_length=1000)
    call_number = models.CharField(max_length=16)
    rate = models.CharField(max_length=1, choices=RATE_CHOSES, default=RATE_CHOSES[4][0])
    time_to_open = models.TimeField()
    time_to_close = models.TimeField()

    def clean(self):
        if self.time_to_close <= self.time_to_open:
            raise ValidationError({"time_to_close": "Closing time must be after opening time."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail_restaurant", kwargs={"pk": self.id})

    def __str__(self):
        return self.name
