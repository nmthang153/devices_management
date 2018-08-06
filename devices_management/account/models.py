from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_bse = models.BooleanField(default=False)
    is_ns = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    if created:
        Role.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_role(sender, instance, **kwargs):
    instance.role.save()