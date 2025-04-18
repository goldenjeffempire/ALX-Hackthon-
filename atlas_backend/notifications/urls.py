from django.urls import path
from .views import NotificationsView, NotificationPreferenceView, send_notification

urlpatterns = [
    path('my/', NotificationsView.as_view(), name='user-notifications'),
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
    path('send_notification/<int:notification_id>/', send_notification, name='send_notification'),
]
