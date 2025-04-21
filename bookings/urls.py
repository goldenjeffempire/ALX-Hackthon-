from django.urls import path
from .views import (
    WorkspaceListView,
    BookingCreateView,
    BookingListView,
    BookingDetailView,
    AvailabilityCheckView,
)

urlpatterns = [
    path("workspaces/", WorkspaceListView.as_view(), name="workspace-list"),
    path("bookings/", BookingListView.as_view(), name="user-bookings"),
    path("bookings/new/", BookingCreateView.as_view(), name="create-booking"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("availability/", AvailabilityCheckView.as_view(), name="check-availability"),
]
