from django.db.models.signals import post_save
from django.dispatch import receiver
from .email import *
from .models import *


@receiver(post_save, sender=News)
def handle_post_save_news(sender, instance, created, **kwargs):
    if created:
        send_news(instance)


@receiver(post_save, sender=Recall)
def handle_post_save_recall(sender, instance, created, **kwargs):
    send_change_recall(instance, created)
