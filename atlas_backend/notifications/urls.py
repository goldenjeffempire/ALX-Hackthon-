from django.urls import path
from .views import UserNotificationsView, NotificationPreferenceView

urlpatterns = [
    path('my/', UserNotificationsView.as_view(), name='user-notifications'),
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
]
