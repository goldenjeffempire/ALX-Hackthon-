from rest_framework import serializers
from .models import ReportRequest

class ReportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRequest
        fields = '__all__'
        read_only_fields = ['user', 'generated_at', 'status']
