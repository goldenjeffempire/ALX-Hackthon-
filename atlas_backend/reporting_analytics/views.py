from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ReportRequest
from .serializers import ReportRequestSerializer
from .utils import generate_report

class ReportRequestView(generics.ListCreateAPIView):
    serializer_class = ReportRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReportRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        generate_report(instance)  # Synchronous call for now
