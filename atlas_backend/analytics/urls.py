from django.urls import path
from .views import (
    BookingVolumeView,
    OccupancyRateView,
    PeakHoursView,
)

urlpatterns = [
    path("volume/", BookingVolumeView.as_view(), name="booking-volume"),
    path("occupancy/", OccupancyRateView.as_view(), name="occupancy-rate"),
    path("peak-hours/", PeakHoursView.as_view(), name="peak-hours"),
]
