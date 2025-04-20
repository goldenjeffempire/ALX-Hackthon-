from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to perform additional tasks when a User is created
    """
    # This is a placeholder for future user-related signals
    # For example, you could send a welcome email when a user is created
    pass
