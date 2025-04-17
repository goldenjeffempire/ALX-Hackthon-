from django.contrib import admin
from .models import Notification, UserNotificationSettings, NotificationPreference

# Registering Notification model with custom admin interface
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'date_sent')
    search_fields = ('user__username', 'notification_type')
    list_filter = ('is_read', 'notification_type')

# Registering UserNotificationSettings model with custom admin interface
@admin.register(UserNotificationSettings)
class UserNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'sms_notifications', 'push_notifications')

# Registering NotificationPreference model
admin.site.register(NotificationPreference)
