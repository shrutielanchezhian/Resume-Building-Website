# resume_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Resume

@receiver(post_save, sender=User)
def create_resume_for_new_user(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")  # Debugging line
        Resume.objects.create(user=instance)  # Create a Resume object for the new user
