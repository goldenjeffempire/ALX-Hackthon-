from django.contrib import admin
from .models import VirtualMeeting

@admin.register(VirtualMeeting)
class VirtualMeetingAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'start_time', 'end_time', 'workspace')
    list_filter = ('platform', 'timezone')
    search_fields = ('user__email',)
