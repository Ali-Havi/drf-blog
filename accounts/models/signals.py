from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .profiles import Profile


@receiver(post_save, sender=get_user_model())
def create_profile_after_user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
