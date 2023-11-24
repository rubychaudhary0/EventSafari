from django.db.models.signals import post_save
from .models import Audience
from django.dispatch import receiver

@receiver(post_save, sender=Audience)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Audience.objects.create(user=instance)


@receiver(post_save, sender=Audience)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()