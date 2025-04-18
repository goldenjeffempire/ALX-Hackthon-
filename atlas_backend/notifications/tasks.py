# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from twilio.rest import Client
from .models import Notification, NotificationSettings
from django.conf import settings

@shared_task
def send_email_notification(notification_id):
    notification = Notification.objects.get(id=notification_id)
    user = notification.user

    # Check if email notifications are enabled for the user
    if user.usersettings.email_notifications:
        send_mail(
            f"New Notification: {notification.notification_type}",
            notification.message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )

@shared_task
def send_sms_notification(notification_id):
    notification = Notification.objects.get(id=notification_id)
    user = notification.user

    # Check if SMS notifications are enabled for the user
    if user.usersettings.sms_notifications:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=notification.message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.profile.phone_number  # Assume the user has a phone number
        )

@shared_task
def send_push_notification(notification_id):
    notification = Notification.objects.get(id=notification_id)
    user = notification.user

    # Check if push notifications are enabled for the user
    if user.usersettings.push_notifications:
        # Push notification service integration (e.g., Firebase, OneSignal)
        pass
