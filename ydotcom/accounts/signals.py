from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile

# This is the receiver function that is run everytime a user is created
# User is the sender which is responsible for for making the notification (to the reciever)
# `post_save` is the signal that is sent at the end of the save method
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()
    