from django.core.exceptions import ValidationError
from django.db import models

from common.models import BaseModel
from food.models import Food
from restaurant.models import Restaurant


class DayOfWeek(BaseModel):
    DAY_CHOICES = (
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    )
    day = models.CharField(max_length=3, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return self.get_day_display()


class Menu(BaseModel):
    name = models.CharField(max_length=120)
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    foods = models.ManyToManyField(Food, related_name="menus", blank=True)
    available_from = models.TimeField()
    available_to = models.TimeField()
    is_active = models.BooleanField(default=True)
    available_days = models.ManyToManyField(DayOfWeek, related_name="menus")

    def clean(self):
        if self.available_from >= self.available_to:
            raise ValidationError({"available_to": "The end time must be after the start time."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
