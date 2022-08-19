from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    """
    Create profile when user is created
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    """
    Add profiles to each other's friend list
    when Relationship with status "accepted" is created
    """
    relship_sender = instance.sender
    relship_receiver = instance.receiver
    if instance.status == "accepted":
        relship_sender.friends.add(relship_receiver.user)
        relship_receiver.friends.add(relship_sender.user)
        relship_sender.save()
        relship_receiver.save()

@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    """
    Delete profiles from each other's friend list 
    when Relationship is deleted 
    """
    relship_sender = instance.sender
    relship_receiver = instance.receiver

    relship_sender.friends.remove(relship_receiver.user)
    relship_receiver.friends.remove(relship_sender.user)
    relship_sender.save()
    relship_receiver.save()
