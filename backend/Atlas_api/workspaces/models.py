from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For UI icons

    def __str__(self):
        return self.name


class WorkspaceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Workspace(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workspaces",
        limit_choices_to={"user_type": User.UserType.OWNER},
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    location = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    max_capacity = models.PositiveIntegerField()
    min_capacity = models.PositiveIntegerField(default=1)
    workspace_type = models.ForeignKey(
        WorkspaceType, on_delete=models.SET_NULL, null=True, blank=True
    )
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to="workspace_thumbnails/", blank=True)

    def clean(self):
        super().clean()
        if self.opening_time and self.closing_time:
            if self.opening_time >= self.closing_time:
                raise ValidationError(
                    {"closing_time": "Closing time must be after opening time"}
                )
        if self.max_capacity <= self.min_capacity:
            raise ValidationError({
                'max_capacity': 'Max capacity must be greater than min capacity'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_open_now(self):
        from django.utils import timezone

        now = timezone.now().time()
        return self.opening_time <= now <= self.closing_time

    def get_opening_hours_display(self):
        """Format opening hours for display"""
        return f"{self.opening_time.strftime('%I:%M %p')} - {self.closing_time.strftime('%I:%M %p')}"

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        ordering = ["-created_at"]
