from rest_framework import serializers
from .models import Workspace, Booking

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["user", "status", "created_at"]

    def validate(self, data):
        # Check for time conflicts
        existing = Booking.objects.filter(
            workspace=data["workspace"],
            start_time__lt=data["end_time"],
            end_time__gt=data["start_time"],
            status="ACTIVE"
        )
        if existing.exists():
            raise serializers.ValidationError("This workspace is already booked for the selected time range.")
        return data
