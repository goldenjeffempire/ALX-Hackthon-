# serializers.py
from rest_framework import serializers
from .models import GoogleCalendarIntegration

class GoogleCalendarIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleCalendarIntegration
        fields = ['user', 'google_token', 'calendar_id']
