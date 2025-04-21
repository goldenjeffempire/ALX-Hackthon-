from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from .models import Booking, Workspace, WorkspaceType
from notifications.services import notify_booking_confirmed

class WorkspaceTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the WorkspaceType model
    """
    class Meta:
        model = WorkspaceType
        fields = [
            'id', 'name', 'type', 'description', 'capacity', 
            'hourly_price', 'image_url', 'amenities', 'is_active'
        ]


class WorkspaceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Workspace model
    """
    workspace_type_details = WorkspaceTypeSerializer(source='workspace_type', read_only=True)

    class Meta:
        model = Workspace
        fields = [
            'id', 'name', 'workspace_type', 'workspace_type_details', 
            'location', 'floor', 'coordinates', 'floor_plan_coordinates',
            'floor_plan_scale', 'floor_plan_rotation', 'availability_start_time',
            'availability_end_time', 'is_available', 'equipment', 'capacity',
            'floor_plan_image', 'notes'
        ]

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model
    """
    user_email = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()
    workspace_details = WorkspaceSerializer(source='workspace', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'user_email', 'user_name', 'workspace', 'workspace_details',
            'title', 'description', 'start_time', 'end_time', 'status', 
            'attendees', 'recurring', 'recurring_pattern', 'duration_minutes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None

    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return None

    def get_duration_minutes(self, obj):
        return obj.duration_minutes()

    def validate(self, data):
        """
        Validate booking data
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        workspace = data.get('workspace')
        attendees = data.get('attendees', 1)

        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time.")

            if start_time < timezone.now():
                raise serializers.ValidationError("Cannot create bookings in the past.")

        if workspace:
            if not workspace.is_available:
                raise serializers.ValidationError(
                    f"Workspace '{workspace.name}' is not available for booking."
                )

            if attendees > workspace.workspace_type.capacity:
                raise serializers.ValidationError(
                    f"This workspace can only accommodate {workspace.workspace_type.capacity} attendees."
                )

            if start_time and workspace.availability_start_time:
                booking_start_time = start_time.time()
                booking_end_time = end_time.time()

                if (booking_start_time < workspace.availability_start_time or 
                    booking_end_time > workspace.availability_end_time):
                    raise serializers.ValidationError(
                        f"This workspace is only available between "
                        f"{workspace.availability_start_time.strftime('%H:%M')} and "
                        f"{workspace.availability_end_time.strftime('%H:%M')}."
                    )

            if start_time and end_time:
                overlapping_query = Q(
                    workspace=workspace,
                    start_time__lt=end_time,
                    end_time__gt=start_time,
                    status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]
                )

                if self.instance:
                    overlapping_bookings = Booking.objects.filter(
                        overlapping_query
                    ).exclude(id=self.instance.id)
                else:
                    overlapping_bookings = Booking.objects.filter(overlapping_query)

                if overlapping_bookings.exists():
                    raise serializers.ValidationError(
                        f"Workspace '{workspace.name}' is already booked during this time slot."
                    )

        return data

class BookingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a booking
    """
    class Meta:
        model = Booking
        fields = ['title', 'description', 'start_time', 'end_time', 'status', 'attendees']

    def validate(self, data):
        if 'status' in data:
            old_status = self.instance.status
            new_status = data['status']

            if old_status in [Booking.STATUS_COMPLETED, Booking.STATUS_CANCELLED]:
                raise serializers.ValidationError(f"Cannot update a {old_status} booking.")

            if new_status == Booking.STATUS_COMPLETED and self.instance.end_time > timezone.now():
                raise serializers.ValidationError("Cannot mark a future booking as completed.")

        return super().validate(data)


class PublicBookingSlotSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing booked slots (without user details)
    """
    class Meta:
        model = Booking
        fields = ['id', 'start_time', 'end_time', 'status']
