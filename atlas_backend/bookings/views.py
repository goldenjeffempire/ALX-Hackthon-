from rest_framework import generics, permissions, status
from .models import Workspace, Booking
from .serializers import WorkspaceSerializer, BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from notifications.tasks import send_booking_reminder
from datetime import timedelta

class WorkspaceListView(generics.ListAPIView):
    queryset = Workspace.objects.filter(is_active=True)
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        booking = serializer.save(user=self.request.user)

        if booking.user.profile.receive_booking_reminders:
            reminder_time = booking.start_time - timedelta(minutes=30)
            send_booking_reminder.apply_async(
                args=[booking.user.email, booking.workspace.name, booking.start_time.isoformat()],
                eta=reminder_time,
            )
class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class AvailabilityCheckView(APIView):
    def get(self, request):
        workspace_id = request.query_params.get("workspace_id")
        start = request.query_params.get("start_time")
        end = request.query_params.get("end_time")

        if not all([workspace_id, start, end]):
            return Response({"detail": "Missing required parameters."}, status=400)

        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            return Response({"detail": "Workspace not found."}, status=404)

        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)

        conflicts = Booking.objects.filter(
            workspace=workspace,
            start_time__lt=end_dt,
            end_time__gt=start_dt,
            status="ACTIVE"
        ).exists()

        return Response({"available": not conflicts}, status=200)

class WorkspaceCreateUpdateView:
permission_classes = [IsAdmin]
