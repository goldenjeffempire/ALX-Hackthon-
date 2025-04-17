from django.urls import path
from .views import UserNotificationsView, NotificationPreferenceView

urlpatterns = [
    path('my/', UserNotificationsView.as_view(), name='user-notifications'),
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
    path('send_notification/<int:notification_id>/', views.send_notification, name='send_notification'),
]
