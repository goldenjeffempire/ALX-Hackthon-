from rest_framework import viewsets, permissions
from .models import VirtualMeeting
from .serializers import VirtualMeetingSerializer
from .permissions import IsCreatorOrAdmin

class VirtualMeetingViewSet(viewsets.ModelViewSet):
    serializer_class = VirtualMeetingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return VirtualMeeting.objects.filter(user=user)

    def perform_create(self, serializer):
        meeting = serializer.save(user=self.request.user)
        # Here you'd call an external API integration (Zoom/Google/Teams)
        # meeting.meeting_link = generate_meeting_link(...)
        # meeting.save()
