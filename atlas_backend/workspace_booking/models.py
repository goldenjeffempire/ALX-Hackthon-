from django.db import models
from django.conf import settings
from django.utils import timezone

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ("boardroom", "Boardroom"),
        ("classroom", "Classroom"),
        ("private_office", "Private Office"),
        ("hot_desk", "Hot Desk"),
    ]

    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.location.name})"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=255)
    is_recurring = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"

    class Meta:
        ordering = ['start_time']
        unique_together = ('room', 'start_time', 'end_time')
