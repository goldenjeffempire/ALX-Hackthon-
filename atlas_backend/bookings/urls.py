from django.urls import path
from .views import WorkspaceListView, BookingListCreateView, BookingDeleteView

urlpatterns = [
    path("workspaces/", WorkspaceListView.as_view(), name="workspace-list"),
    path("", BookingListCreateView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingDeleteView.as_view(), name="booking-delete"),
]
