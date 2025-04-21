from django.urls import path

from .views import DashboardStatsView, BookingMetricsView

app_name = 'dashboard'

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('metrics/', BookingMetricsView.as_view(), name='booking_metrics'),
]
