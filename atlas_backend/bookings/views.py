from rest_framework import generics, permissions
from .models import Workspace, Booking
from .serializers import WorkspaceSerializer, BookingSerializer

class WorkspaceListView(generics.ListAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingDeleteView(generics.DestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
