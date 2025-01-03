from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
import logging

CustomUser = get_user_model()

@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            contact_email=instance.email  
        )
        logging.info(f"Profile created for user {instance.username}.")
    else:
        profile = instance.profile
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.contact_email = instance.email
        profile.save()
        logging.info(f"Profile updated for user {instance.username}.")

