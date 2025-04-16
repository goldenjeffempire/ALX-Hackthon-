from django.urls import path
from .views import RoomListView, BookingListCreateView, BookingDetailView

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
]
