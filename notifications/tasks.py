from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_reminder(email, workspace_name, start_time):
    subject = "Upcoming Booking Reminder"
    message = f"Reminder: You have a booking for '{workspace_name}' at {start_time}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
