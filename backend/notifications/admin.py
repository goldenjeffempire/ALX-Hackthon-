from django.contrib import admin
from .models import Notification, NotificationPreference, AnnouncementGroup, Announcement


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'message', 'notification_type', 'is_read')
        }),
        ('Related Object', {
            'fields': ('related_object_type', 'related_object_id')
        }),
        ('Scheduling', {
            'fields': ('scheduled_for',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'daily_digest', 'weekly_digest')
    list_filter = ('daily_digest', 'weekly_digest')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Booking Notifications', {
            'fields': ('booking_confirmation', 'booking_reminder', 'booking_cancellation')
        }),
        ('Waitlist Notifications', {
            'fields': ('waitlist_fulfilled',)
        }),
        ('System Notifications', {
            'fields': ('system_announcements', 'maintenance_alerts')
        }),
        ('Digest Settings', {
            'fields': ('daily_digest', 'weekly_digest', 'quiet_hours_start', 'quiet_hours_end')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnnouncementGroup)
class AnnouncementGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sender', 'is_global', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_global', 'is_active', 'start_date')
    search_fields = ('title', 'message', 'sender__email')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'message', 'sender')
        }),
        ('Target Audience', {
            'fields': ('is_global', 'target_groups')
        }),
        ('Visibility Settings', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
