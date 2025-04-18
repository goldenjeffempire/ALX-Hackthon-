from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualMeetingViewSet

router = DefaultRouter()
router.register(r'meetings', VirtualMeetingViewSet, basename='virtualmeeting')

urlpatterns = [
    path('', include(router.urls)),
]
