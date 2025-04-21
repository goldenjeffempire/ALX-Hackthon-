from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookingViewSet, PublicBookedSlotsView,
    WorkspaceTypeViewSet, WorkspaceViewSet
)

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'workspace-types', WorkspaceTypeViewSet, basename='workspace-type')
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')

app_name = 'bookings'

urlpatterns = [
    path('', include(router.urls)),
    path('slots/', PublicBookedSlotsView.as_view(), name='public-booked-slots'),
]
