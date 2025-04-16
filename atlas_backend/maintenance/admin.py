from django.contrib import admin
from .models import MaintenanceRequest

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'workspace', 'user', 'submitted_at')
    list_filter = ('status', 'priority', 'workspace')
    search_fields = ('title', 'description')
