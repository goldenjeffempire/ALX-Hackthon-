from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()

class WorkspaceType(models.Model):
    """
    Model for workspace types (desk, meeting room, event space, etc.)
    """
    TYPE_DESK = 'desk'
    TYPE_MEETING_ROOM = 'meeting_room'
    TYPE_EVENT_SPACE = 'event_space'
    
    TYPE_CHOICES = (
        (TYPE_DESK, 'Desk'),
        (TYPE_MEETING_ROOM, 'Meeting Room'),
        (TYPE_EVENT_SPACE, 'Event Space'),
    )
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=1)
    hourly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_url = models.URLField(blank=True, null=True)
    amenities = models.JSONField(default=list, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Workspace(models.Model):
    """
    Model for individual workspaces (specific desk, room, etc.)
    """
    name = models.CharField(max_length=100)
    workspace_type = models.ForeignKey(WorkspaceType, on_delete=models.CASCADE, related_name='workspaces')
    location = models.CharField(max_length=255)
    floor = models.CharField(max_length=50, blank=True, null=True)
    coordinates = models.JSONField(default=dict, blank=True, null=True)  # For floor plan positioning
    floor_plan_coordinates = models.JSONField(default=dict, blank=True, null=True)  # {x, y, width, height}
    floor_plan_scale = models.FloatField(default=1.0)  # Scale factor for floor plan
    floor_plan_rotation = models.FloatField(default=0.0)  # Rotation in degrees
    availability_start_time = models.TimeField(default='08:00')
    availability_end_time = models.TimeField(default='18:00')
    is_available = models.BooleanField(default=True)
    equipment = models.JSONField(default=list, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=1)
    floor_plan_image = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.workspace_type.name}"
    
    
class Booking(models.Model):
    """
    Model for workspace bookings
    """
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='bookings')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    attendees = models.PositiveIntegerField(default=1)
    recurring = models.BooleanField(default=False)
    recurring_pattern = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
        # Add a constraint to ensure that end_time is after start_time
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='end_time_after_start_time'
            )
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
    
    def clean(self):
        """
        Enhanced validation for bookings
        """
        if self.workspace:
            # Validate business hours
            workspace_start = self.workspace.availability_start_time
            workspace_end = self.workspace.availability_end_time
            booking_start = self.start_time.time()
            booking_end = self.end_time.time()

            if booking_start < workspace_start or booking_end > workspace_end:
                raise ValidationError(
                    f"Bookings must be within business hours: "
                    f"{workspace_start.strftime('%H:%M')} - {workspace_end.strftime('%H:%M')}"
                )

            # Validate minimum and maximum duration
            duration = (self.end_time - self.start_time).total_seconds() / 3600
            if duration < 0.5:  # 30 minutes minimum
                raise ValidationError("Bookings must be at least 30 minutes long")
            if duration > 8:  # 8 hours maximum
                raise ValidationError("Bookings cannot exceed 8 hours")

            # Validate advance booking
            advance_hours = (self.start_time - timezone.now()).total_seconds() / 3600
            if advance_hours < 0:
                raise ValidationError("Cannot create bookings in the past")
            if advance_hours > 720:  # 30 days
                raise ValidationError("Cannot book more than 30 days in advance")
            # Check if the workspace can accommodate the attendees
            if self.attendees > self.workspace.workspace_type.capacity:
                raise ValidationError(f"This workspace can only accommodate {self.workspace.workspace_type.capacity} attendees")
            
            # Check for booking conflicts (overlapping bookings for the same workspace)
            overlapping_bookings = Booking.objects.filter(
                workspace=self.workspace,
                status__in=[self.STATUS_PENDING, self.STATUS_CONFIRMED],
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
            
            # Exclude the current booking in case of updates
            if self.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)
            
            if overlapping_bookings.exists():
                raise ValidationError("This workspace is already booked during the selected time")
    
    def __init__(self, *args, **kwargs):
        """
        Override init to track status changes
        """
        super().__init__(*args, **kwargs)
        # Store original status to track changes
        if self.pk:
            self._old_status = self.status
    
    def save(self, *args, **kwargs):
        """
        Override save method to perform validation before saving
        """
        # For existing bookings, check if status has changed
        if self.pk:
            try:
                old_booking = Booking.objects.get(pk=self.pk)
                if old_booking.status != self.status:
                    # Store old status for signal handler to use
                    self._old_status = old_booking.status
            except Booking.DoesNotExist:
                pass
                
        # For new bookings
        if not self.pk:
            self._old_status = None
            
        self.clean()
        super().save(*args, **kwargs)
    
    def is_active(self):
        """
        Returns True if the booking is active (not cancelled or completed)
        """
        return self.status in [self.STATUS_PENDING, self.STATUS_CONFIRMED]
    
    def is_upcoming(self):
        """
        Returns True if the booking is in the future
        """
        return self.start_time > timezone.now()
    
    def duration_minutes(self):
        """
        Returns the duration of the booking in minutes
        """
        duration = self.end_time - self.start_time
        return int(duration.total_seconds() / 60)
    
    def cancel(self):
        """
        Cancels the booking
        """
        self.status = self.STATUS_CANCELLED
        self.save()
        
    def confirm(self):
        """
        Confirms the booking
        """
        self.status = self.STATUS_CONFIRMED
        self.save()
        
    def complete(self):
        """
        Marks the booking as completed
        """
        self.status = self.STATUS_COMPLETED
        self.save()
