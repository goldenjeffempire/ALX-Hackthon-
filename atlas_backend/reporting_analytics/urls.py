from django.urls import path
from .views import ReportRequestView

urlpatterns = [
    path('requests/', ReportRequestView.as_view(), name='report-requests'),
]
