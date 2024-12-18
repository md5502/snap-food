import random
import string

from django.db import models

from common.models import BaseModel
from food.models import Food
from users.models import CustomUser


def generate_tracking_code():
    prefix = "ORDER"
    random_string = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))  # noqa: S311
    return f"{prefix}-{random_string}"


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELLED = "CANCELLED", "Cancelled"


class Order(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    track_number = models.CharField(max_length=20, unique=True, default=generate_tracking_code, null=True, blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.track_number} - {self.get_status_display()}"

    def update_status(self, new_status):
        """Update the status of the order."""
        if new_status not in OrderStatus.values:
            raise ValueError("Invalid status.")
        self.status = new_status
        self.save()

    def calculate_total(self):
        """Calculate the total amount of the order based on related items."""
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
