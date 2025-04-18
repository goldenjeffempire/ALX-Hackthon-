from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import Notification, NotificationPreference, NotificationSettings
from .tasks import send_email_notification, send_sms_notification, send_push_notification
from .serializers import NotificationSerializer, NotificationPreferenceSerializer

# View for sending a notification and triggering async tasks
def send_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)

        # Send email, SMS, and push notifications asynchronously
        send_email_notification.delay(notification.id)
        send_sms_notification.delay(notification.id)
        send_push_notification.delay(notification.id)
        return JsonResponse({"status": "Notification sent successfully!"}, status=200)
    except Notification.DoesNotExist:
        return JsonResponse({"error": "Notification not found!"}, status=404)

# View for listing user notifications
class NotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-sent_at')

# View for retrieving and updating user notification preferences
class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Creates NotificationPreference if not already present for user
        pref, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return pref
