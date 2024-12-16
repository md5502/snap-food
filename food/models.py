from django.core.exceptions import ValidationError
from django.db import models

from common.models import BaseModel
from restaurant.models import Restaurant


class Food(BaseModel):
    RATE_CHOSES = (
        ("1", "very bad"),
        ("2", "bad"),
        ("3", "natural"),
        ("4", "good"),
        ("5", "very good"),
    )

    name = models.CharField(max_length=120)
    description = models.TextField()

    image = models.ImageField(default="foods/default.jpg", upload_to="foods")
    count = models.PositiveIntegerField()
    rate = models.CharField(max_length=1, choices=RATE_CHOSES, default=RATE_CHOSES[4][0])
    discount = models.PositiveIntegerField(default=0)
    price = models.PositiveBigIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="foods")

    def clean(self):
        if self.discount <= 0 and self.discount >= 99:  # noqa: PLR2004
            raise ValidationError({"discount": "Discount should start from 0 to 99"})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
