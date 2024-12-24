from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(signal=post_save, sender=Order)
def send_notification_for_restaurant(sender, instance, created, **kwargs):
    restaurants = {}
    items = sender.items
    for item in items:
        restaurants[item.product.restaurant.pk] = []

    for item in items:
        restaurants[item.product.restaurant.pk].append(item)
