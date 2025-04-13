# Notifications MOdels
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Model for user notifications
    """
    NOTIFICATION_TYPES = (
        ('booking', 'Booking'),
        ('cancellation', 'Cancellation'),
        ('reminder', 'Reminder'),
        ('waitlist', 'Waitlist'),
        ('admin', 'Administrative'),
        ('system', 'System'),
    )

    RELATED_OBJECT_TYPES = (
        ('booking', 'Booking'),
        ('workspace', 'Workspace'),
        ('waitlist', 'Waitlist Entry'),
        ('user', 'User'),
        ('none', 'None'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    # For linking to related objects
    related_object_type = models.CharField(max_length=20, choices=RELATED_OBJECT_TYPES, default='none')
    related_object_id = models.PositiveIntegerField(null=True, blank=True)

    # Status fields
    is_read = models.BooleanField(default=False)

    # Scheduled delivery (for scheduled notifications)
    scheduled_for = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['scheduled_for']),
        ]

    def __str__(self):
        return f"Notification for {self.user.email}: {self.title}"


class NotificationPreference(models.Model):
    """
    User preferences for notifications
    """
    NOTIFICATION_CHANNELS = (
        ('email', 'Email'),
        ('in_app', 'In-App'),
        ('push', 'Push Notification'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )

    # Booking notifications
    booking_confirmation = models.JSONField(default=list)  # List of channels
    booking_reminder = models.JSONField(default=list)
    booking_cancellation = models.JSONField(default=list)

    # Waitlist notifications
    waitlist_fulfilled = models.JSONField(default=list)

    # System notifications
    system_announcements = models.JSONField(default=list)
    maintenance_alerts = models.JSONField(default=list)

    # Digest settings
    daily_digest = models.BooleanField(default=False)
    weekly_digest = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification preferences for {self.user.email}"


class AnnouncementGroup(models.Model):
    """
    Groups for sending targeted announcements
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Target criteria - can be department, role, or specific users
    criteria = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    """
    Administrative announcements
    """
    title = models.CharField(max_length=255)
    message = models.TextField()

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_announcements'
    )

    # Target audience
    is_global = models.BooleanField(default=False)
    target_groups = models.ManyToManyField(AnnouncementGroup, blank=True)

    # Visibility settings
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    # Status
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

