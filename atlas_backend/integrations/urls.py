# urls.py
from django.urls import path
from .views import GoogleCalendarSync

urlpatterns = [
    path('google_calendar_sync/', GoogleCalendarSync.as_view(), name='google_calendar_sync'),
    # Add paths for Microsoft, Slack, Trello, and Asana
]
