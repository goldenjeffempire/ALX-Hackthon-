from django.db import models
from workspace_booking.models import Location

class FloorPlan(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='floor_plans')
    name = models.CharField(max_length=255)
    svg_map = models.TextField(help_text="SVG or base64 encoded floor map")

    def __str__(self):
        return f"{self.name} - {self.location.name}"

class Workspace(models.Model):
    ROOM_CONFIG_CHOICES = [
        ('boardroom', 'Boardroom'),
        ('classroom', 'Classroom'),
        ('pod', 'Pod'),
        ('open_desk', 'Open Desk'),
    ]

    name = models.CharField(max_length=255)
    floor_plan = models.ForeignKey(FloorPlan, on_delete=models.CASCADE, related_name='workspaces')
    config_type = models.CharField(max_length=50, choices=ROOM_CONFIG_CHOICES)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    live_status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance')
    ], default='available')

    def __str__(self):
        return f"{self.name} ({self.config_type})"
