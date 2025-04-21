from django.utils import timezone
from django.db.models import Q, Count
from rest_framework import viewsets, permissions, status, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime

from .models import Booking, Workspace, WorkspaceType
from .serializers import (
    BookingSerializer, BookingUpdateSerializer, PublicBookingSlotSerializer,
    WorkspaceSerializer, WorkspaceTypeSerializer
)

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to only allow owners of an object or admins to view/edit it
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.user == request.user


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on bookings
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['start_time']
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return BookingUpdateSerializer
        return BookingSerializer
    
    def get_queryset(self):
        """
        Filter bookings to return only those belonging to the current user
        unless the user is an admin
        """
        if self.request.user.is_admin:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Custom action to cancel a booking
        """
        booking = self.get_object()
        
        if booking.status in [Booking.STATUS_COMPLETED, Booking.STATUS_CANCELLED]:
            return Response(
                {"detail": f"Cannot cancel a booking with status '{booking.status}'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.cancel()
        return Response({"status": "Booking cancelled"})
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Custom action to confirm a booking (admin only)
        """
        if not request.user.is_admin:
            return Response(
                {"detail": "Only administrators can confirm bookings"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking = self.get_object()
        
        if booking.status != Booking.STATUS_PENDING:
            return Response(
                {"detail": "Only pending bookings can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.confirm()
        return Response({"status": "Booking confirmed"})
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Filter to only show upcoming bookings for the current user
        """
        queryset = self.get_queryset().filter(
            start_time__gt=timezone.now()
        ).order_by('start_time')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """
        Filter to only show past bookings for the current user
        """
        queryset = self.get_queryset().filter(
            end_time__lt=timezone.now()
        ).order_by('-start_time')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PublicBookedSlotsView(generics.ListAPIView):
    """
    Public API to fetch booked slots for a specific date
    """
    serializer_class = PublicBookingSlotSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """
        Filter bookings by date if provided in query params
        """
        date_str = self.request.query_params.get('date', None)
        workspace_id = self.request.query_params.get('workspace', None)
        
        queryset = Booking.objects.filter(
            status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]
        )
        
        # Filter by workspace if specified
        if workspace_id:
            try:
                queryset = queryset.filter(workspace_id=int(workspace_id))
            except (ValueError, TypeError):
                return Booking.objects.none()
        
        # Filter by date if specified
        if date_str:
            try:
                year, month, day = map(int, date_str.split('-'))
                
                # Get all bookings for the specified date
                queryset = queryset.filter(
                    Q(start_time__year=year, start_time__month=month, start_time__day=day) |
                    Q(end_time__year=year, end_time__month=month, end_time__day=day)
                )
            except (ValueError, TypeError):
                # If date format is invalid, return an empty queryset
                return Booking.objects.none()
        
        return queryset


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow admins to create, update or delete,
    but allow anyone to view
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admins
        return request.user.is_authenticated and request.user.is_admin


class WorkspaceTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workspace types
    """
    queryset = WorkspaceType.objects.all()
    serializer_class = WorkspaceTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'type', 'capacity', 'hourly_price']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Filter to only show active workspace types
        """
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WorkspaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workspaces
    """
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'workspace_type': ['exact'],
        'location': ['exact', 'icontains'],
        'floor': ['exact'],
        'is_available': ['exact'],
        'capacity': ['gte', 'lte'],
        'workspace_type__amenities': ['contains'],
        'equipment': ['contains']
    }
    search_fields = ['name', 'location', 'notes', 'equipment']
    ordering_fields = ['name', 'location', 'workspace_type__name', 'capacity']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)

        if all([date, start_time, end_time]):
            try:
                datetime_start = timezone.datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
                datetime_end = timezone.datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
                
                booked_workspaces = Booking.objects.filter(
                    start_time__lt=datetime_end,
                    end_time__gt=datetime_start,
                    status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]
                ).values_list('workspace_id', flat=True)
                
                queryset = queryset.exclude(id__in=booked_workspaces)
            except ValueError:
                pass

        return queryset
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Filter to only show available workspaces
        """
        queryset = self.get_queryset().filter(is_available=True)
        
        # Filter by date and time if provided
        date_str = request.query_params.get('date', None)
        start_time_str = request.query_params.get('start_time', None)
        end_time_str = request.query_params.get('end_time', None)
        
        if date_str and start_time_str and end_time_str:
            try:
                # Parse the date and times
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                start_time = datetime.strptime(f"{date_str} {start_time_str}", '%Y-%m-%d %H:%M').replace(tzinfo=timezone.get_current_timezone())
                end_time = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M').replace(tzinfo=timezone.get_current_timezone())
                
                # Find workspaces with conflicting bookings
                booked_workspace_ids = Booking.objects.filter(
                    status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED],
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).values_list('workspace_id', flat=True)
                
                # Exclude workspaces with conflicting bookings
                queryset = queryset.exclude(id__in=booked_workspace_ids)
                
            except (ValueError, TypeError):
                # If date/time format is invalid, continue without time filtering
                pass
        
        # Filter by capacity if provided
        capacity = request.query_params.get('capacity', None)
        if capacity:
            try:
                capacity = int(capacity)
                queryset = queryset.filter(workspace_type__capacity__gte=capacity)
            except (ValueError, TypeError):
                pass
        
        # Filter by type if provided
        workspace_type = request.query_params.get('type', None)
        if workspace_type:
            queryset = queryset.filter(workspace_type__type=workspace_type)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """
        Get all bookings for a specific workspace
        """
        workspace = self.get_object()
        
        # Get start and end dates for filtering if provided
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        bookings = workspace.bookings.filter(
            status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]
        )
        
        # Apply date filters if provided
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
                bookings = bookings.filter(end_time__gte=start_date)
            except (ValueError, TypeError):
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.get_current_timezone())
                end_date = end_date.replace(hour=23, minute=59, second=59)
                bookings = bookings.filter(start_time__lte=end_date)
            except (ValueError, TypeError):
                pass
        
        # Use the public booking serializer to exclude sensitive info
        serializer = PublicBookingSlotSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def floor_plan(self, request):
        """
        Get workspaces organized by floor with their floor plan data
        """
        floor = request.query_params.get('floor', None)
        queryset = self.get_queryset()
        
        if floor:
            queryset = queryset.filter(floor=floor)
        
        workspaces = queryset.values(
            'id', 'name', 'floor', 'floor_plan_coordinates',
            'floor_plan_scale', 'floor_plan_rotation',
            'floor_plan_image', 'is_available'
        ).order_by('floor', 'name')
        
        # Group by floor
        floors = {}
        for workspace in workspaces:
            floor_key = workspace['floor'] or 'unassigned'
            if floor_key not in floors:
                floors[floor_key] = []
            floors[floor_key].append(workspace)
        
        return Response(floors)

    @action(detail=True, methods=['patch'])
    def update_position(self, request, pk=None):
        """
        Update workspace position on floor plan
        """
        if not request.user.is_admin:
            return Response(
                {"detail": "Only administrators can update workspace positions"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        workspace = self.get_object()
        serializer = self.get_serializer(
            workspace,
            data={
                'floor_plan_coordinates': request.data.get('coordinates', {}),
                'floor_plan_scale': request.data.get('scale', 1.0),
                'floor_plan_rotation': request.data.get('rotation', 0.0)
            },
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get booking statistics by workspace (admin only)
        """
        if not request.user.is_authenticated or not request.user.is_admin:
            return Response(
                {"detail": "Only administrators can access statistics"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get all workspaces with their booking counts
        workspaces = Workspace.objects.annotate(
            total_bookings=Count('bookings'),
            active_bookings=Count('bookings', filter=Q(
                bookings__status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED],
                bookings__end_time__gt=timezone.now()
            ))
        )
        
        # Create a simple stats object for each workspace
        stats = []
        for workspace in workspaces:
            stats.append({
                'id': workspace.id,
                'name': workspace.name,
                'location': workspace.location,
                'type': workspace.workspace_type.get_type_display(),
                'total_bookings': workspace.total_bookings,
                'active_bookings': workspace.active_bookings,
                'is_available': workspace.is_available
            })
        
        return Response(stats)
