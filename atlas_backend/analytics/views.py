from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Avg, F
from django.utils.timezone import now, timedelta
from bookings.models import Booking, Workspace
from django.db.models.functions import ExtractHour


class BookingVolumeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        last_30_days = now() - timedelta(days=30)
        data = (
            Booking.objects.filter(created_at__gte=last_30_days)
            .extra(select={"day": "date(created_at)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        return Response(data)


class OccupancyRateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_workspaces = Workspace.objects.count()
        active_bookings = (
            Booking.objects.filter(status="ACTIVE").count()
        )
        rate = (active_bookings / total_workspaces) * 100 if total_workspaces else 0
        return Response({"occupancy_rate_percent": round(rate, 2)})


class PeakHoursView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            Booking.objects.annotate(hour=ExtractHour("start_time"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )
        return Response(data)
