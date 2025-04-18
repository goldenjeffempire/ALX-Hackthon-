from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_settings')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.user.username}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('booking', 'Booking Confirmation'),
        ('maintenance', 'Maintenance Alert'),
        ('system', 'System Alert'),
        ('reminder', 'Reminder'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Renamed from 'read' to 'is_read'
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} ({self.notification_type})"

# Notification preference model that handles the user's notification choices for email, SMS, and push
class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email}'s Preferences"
