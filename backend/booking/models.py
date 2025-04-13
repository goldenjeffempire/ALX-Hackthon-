from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class WorkspaceType(models.Model):
    """ example: Meeting room, Private Office, Open Desk """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkspaceAmenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workspace(models.Model):
    """ Class that holds basic information about workspaces"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    amenities = models.CharField(max_length=255)
    workspace_type = models.ForeignKey(WorkspaceType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(WorkspaceAmenity)
    # default value is admin
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces', default=1)

    def __str__(self):
        return self.name


class Booking(models.Model):
    """  """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
         ('cancelled', 'Cancelled'),
         ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workspace.name} ({self.start_time})"


class UserProfile(models.Model):
    """User Profile model 
    Use this class to avoid issues in django"""
    USER_ROLES = (
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('client', 'Client'),
            )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"

