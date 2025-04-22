from django.db import models
from django.conf import settings

class Workspace(models.Model):
    WORKSPACE_TYPE_CHOICES = [
        ("DESK", "Desk"),
        ("ROOM", "Room"),
        ("SPACE", "Open Space"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=WORKSPACE_TYPE_CHOICES)
    capacity = models.PositiveIntegerField(default=1)
    features = models.JSONField(blank=True, default=dict)  # e.g. {"monitor": True, "whiteboard": False}
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "start_time", "end_time"], name="unique_workspace_booking"
            )
        ]

    def __str__(self):
        return f"{self.user.email} -> {self.workspace.name} ({self.start_time} - {self.end_time})"
