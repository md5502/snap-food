from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, email=instance.email)
    elif instance.profile.email != instance.email:
        instance.profile.email = instance.email
        instance.profile.save()


@receiver(post_save, sender=UserProfile)
def update_user_from_profile(sender, instance, **kwargs):
    user = instance.user
    if user.email != instance.email:
        user.email = instance.email
        user.save()

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
