from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'workspace', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating')
    search_fields = ('user__email', 'workspace__name')
