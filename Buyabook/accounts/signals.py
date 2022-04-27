from django.core import signals
from django.db.models.signals import post_save

from django.dispatch import receiver
from .models import Profile, BaBUser

# TODO
"""
@receiver(post_save, sender=BaBUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def delete_user(sender, instance, deleted, **kwargs):
    if deleted:
        BaBUser.objects.delete(user=instance)

"""