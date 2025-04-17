from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address', 'details')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'action')
