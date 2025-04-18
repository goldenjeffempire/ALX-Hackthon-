# integrations/models.py
from django.db import models
from django.conf import settings  # <-- ✅ NEW IMPORT

class GoogleCalendarIntegration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- ✅ FIXED
    google_token = models.CharField(max_length=512)
    calendar_id = models.CharField(max_length=255)

class MicrosoftCalendarIntegration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- ✅ FIXED
    microsoft_token = models.CharField(max_length=512)
    calendar_id = models.CharField(max_length=255)

class SlackIntegration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- ✅ FIXED
    slack_token = models.CharField(max_length=512)

class TrelloIntegration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- ✅ FIXED
    trello_token = models.CharField(max_length=512)
    board_id = models.CharField(max_length=255)

class AsanaIntegration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- ✅ FIXED
    asana_token = models.CharField(max_length=512)
    workspace_id = models.CharField(max_length=255)
