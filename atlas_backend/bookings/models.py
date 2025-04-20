from django.db import models
from django.contrib.auth.models import User

class Workspace(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.location}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.workspace.name} on {self.date} ({self.time_slot})"
