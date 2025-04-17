from rest_framework import serializers
from .models import VirtualMeeting

class VirtualMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMeeting
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'meeting_link']
