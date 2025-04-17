from rest_framework import viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer
from .permissions import IsAdminOrReadOnly

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return AuditLog.objects.all()
