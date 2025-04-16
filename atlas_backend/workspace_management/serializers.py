from rest_framework import serializers
from .models import FloorPlan, Workspace
from workspace_booking.serializers import LocationSerializer
from user_management.models import Location


class FloorPlanSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source='location', write_only=True)

    class Meta:
        model = FloorPlan
        fields = ['id', 'name', 'svg_map', 'location', 'location_id']

class WorkspaceSerializer(serializers.ModelSerializer):
    floor_plan = FloorPlanSerializer(read_only=True)
    floor_plan_id = serializers.PrimaryKeyRelatedField(queryset=FloorPlan.objects.all(), source='floor_plan', write_only=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'config_type', 'capacity', 'live_status', 'is_active', 'floor_plan', 'floor_plan_id']
