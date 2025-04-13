# Notifications Models
from rest_framework import serializers
from .models import Notification, NotificationPreference, AnnouncementGroup, Announcement


class NotificationSerializer(serializers.ModelSerializer):
    related_link = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'title', 'message', 'notification_type',
            'related_object_type', 'related_object_id', 'related_link',
            'is_read', 'scheduled_for', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_related_link(self, obj):
        """
        Generate a frontend-friendly link to the related object
        """
        if obj.related_object_type == 'booking' and obj.related_object_id:
            return f"/bookings/{obj.related_object_id}"
        elif obj.related_object_type == 'workspace' and obj.related_object_id:
            return f"/workspaces/{obj.related_object_id}"
        elif obj.related_object_type == 'waitlist' and obj.related_object_id:
            return f"/bookings/waitlist/{obj.related_object_id}"
        return None


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'booking_confirmation', 'booking_reminder',
            'booking_cancellation', 'waitlist_fulfilled', 'system_announcements',
            'maintenance_alerts', 'daily_digest', 'weekly_digest',
            'quiet_hours_start', 'quiet_hours_end', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class AnnouncementGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementGroup
        fields = ['id', 'name', 'description', 'criteria', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'message', 'sender', 'sender_name',
            'is_global', 'target_groups', 'start_date', 'end_date',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}" if obj.sender else "System"


class CreateAnnouncementSerializer(serializers.ModelSerializer):
    target_group_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        model = Announcement
        fields = [
            'title', 'message', 'is_global', 'target_group_ids',
            'start_date', 'end_date', 'is_active'
        ]

    def create(self, validated_data):
        target_group_ids = validated_data.pop('target_group_ids', [])

        # Set the current user as the sender
        validated_data['sender'] = self.context['request'].user

        announcement = Announcement.objects.create(**validated_data)

        # Add target groups if provided
        if target_group_ids and not validated_data.get('is_global', False):
            announcement.target_groups.set(AnnouncementGroup.objects.filter(id__in=target_group_ids))

        return announcement
