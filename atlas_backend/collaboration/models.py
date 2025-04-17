from django.db import models
from django.conf import settings
from workspace_management.models import Workspace

class VirtualMeeting(models.Model):
    PLATFORM_CHOICES = [
        ('zoom', 'Zoom'),
        ('google_meet', 'Google Meet'),
        ('ms_teams', 'Microsoft Teams'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    meeting_link = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    timezone = models.CharField(max_length=100, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform.upper()} - {self.user.email} @ {self.start_time}"
