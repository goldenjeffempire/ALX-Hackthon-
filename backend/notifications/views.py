from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notification, NotificationPreference, AnnouncementGroup, Announcement
from .serializers import (
    NotificationSerializer, NotificationPreferenceSerializer,
    AnnouncementGroupSerializer, AnnouncementSerializer, CreateAnnouncementSerializer
)
from users.permissions import IsAdminOrSelf, IsAdminOrReadOnly
from django.db import models


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_read', 'related_object_type']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()

        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"status": "All notifications marked as read"})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get the count of unread notifications"""
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({"unread_count": count})


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        user = self.request.user

        # For admin users, allow access to all preferences
        if user.is_staff or user.role == 'admin':
            return NotificationPreference.objects.all()

        # Regular users can only access their own preferences
        return NotificationPreference.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        # Check if preferences already exist for this user
        if NotificationPreference.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Notification preferences already exist for this user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new preferences with the user from the request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get the current user's notification preferences"""
        try:
            preferences = NotificationPreference.objects.get(user=request.user)
            serializer = self.get_serializer(preferences)
            return Response(serializer.data)
        except NotificationPreference.DoesNotExist:
            # Create default preferences for the user
            preferences = NotificationPreference.objects.create(
                user=request.user,
                booking_confirmation=['email', 'in_app'],
                booking_reminder=['email', 'in_app'],
                booking_cancellation=['email', 'in_app'],
                waitlist_fulfilled=['email', 'in_app'],
                system_announcements=['in_app'],
                maintenance_alerts=['email', 'in_app'],
            )
            serializer = self.get_serializer(preferences)
            return Response(serializer.data)


class AnnouncementGroupViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementGroup.objects.all().order_by('name')
    serializer_class = AnnouncementGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class AnnouncementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_global', 'is_active']
    search_fields = ['title', 'message']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']

    def get_queryset(self):
        # For regular users, only return active announcements that are either global or targeted to their groups
        user = self.request.user
        now = timezone.now()

        if user.is_staff or user.role == 'admin':
            # Admin users can see all announcements
            return Announcement.objects.all()

        # Regular users see only currently active announcements
        return Announcement.objects.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            # Apply end date filter if it exists
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        ).filter(
            # Either global announcements or targeted to the user's department/role
            models.Q(is_global=True) |
            models.Q(target_groups__criteria__department=user.department) |
            models.Q(target_groups__criteria__role=user.role)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateAnnouncementSerializer
        return AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
