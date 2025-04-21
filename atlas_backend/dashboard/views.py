from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import views, permissions, status
from rest_framework.response import Response
from datetime import timedelta

from bookings.models import Booking
from accounts.models import User

class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access the dashboard
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class DashboardStatsView(views.APIView):
    """
    View to return dashboard statistics based on user role
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_admin_stats(self, request):
        # Get counts for key metrics
        total_users = User.objects.count()
        active_users = User.objects.filter(bookings__isnull=False).distinct().count()
        
        total_bookings = Booking.objects.count()
        active_bookings = Booking.objects.filter(
            status__in=['pending', 'confirmed'],
            end_time__gt=timezone.now()
        ).count()
        
        # Get bookings per day for the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        bookings_per_day = (
            Booking.objects
            .filter(created_at__gte=thirty_days_ago)
            .extra({'date': "date(created_at)"})
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        
        # Get bookings by status
        bookings_by_status = (
            Booking.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        
        return {
            'user_stats': {
                'total_users': total_users,
                'active_users': active_users,
            },
            'booking_stats': {
                'total_bookings': total_bookings,
                'active_bookings': active_bookings,
                'by_status': {
                    item['status']: item['count'] for item in bookings_by_status
                }
            },
            'bookings_per_day': [
                {'date': item['date'], 'count': item['count']} 
                for item in bookings_per_day
            ]
        }

    def get_employee_stats(self, request):
        user_bookings = Booking.objects.filter(user=request.user)
        active_bookings = user_bookings.filter(
            status__in=['pending', 'confirmed'],
            end_time__gt=timezone.now()
        ).count()
        
        # Get personal bookings per day
        thirty_days_ago = timezone.now() - timedelta(days=30)
        personal_bookings_per_day = (
            user_bookings
            .filter(created_at__gte=thirty_days_ago)
            .extra({'date': "date(created_at)"})
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        
        return {
            'personal_stats': {
                'total_bookings': user_bookings.count(),
                'active_bookings': active_bookings,
                'by_status': {
                    status: user_bookings.filter(status=status).count()
                    for status in ['pending', 'confirmed', 'cancelled', 'completed']
                }
            },
            'bookings_per_day': [
                {'date': item['date'], 'count': item['count']} 
                for item in personal_bookings_per_day
            ]
        }

    def get(self, request):
        if request.user.role == User.ROLE_ADMIN:
            return Response(self.get_admin_stats(request))
        else:
            return Response(self.get_employee_stats(request))
    
    def get(self, request):
        # Get counts for key metrics
        total_users = User.objects.count()
        active_users = User.objects.filter(bookings__isnull=False).distinct().count()
        
        total_bookings = Booking.objects.count()
        active_bookings = Booking.objects.filter(
            status__in=['pending', 'confirmed'],
            end_time__gt=timezone.now()
        ).count()
        
        # Get bookings per day for the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        bookings_per_day = (
            Booking.objects
            .filter(created_at__gte=thirty_days_ago)
            .extra({'date': "date(created_at)"})
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        
        # Get bookings by status
        bookings_by_status = (
            Booking.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        
        # Format the response data
        data = {
            'user_stats': {
                'total_users': total_users,
                'active_users': active_users,
            },
            'booking_stats': {
                'total_bookings': total_bookings,
                'active_bookings': active_bookings,
                'by_status': {
                    item['status']: item['count'] for item in bookings_by_status
                }
            },
            'bookings_per_day': [
                {'date': item['date'], 'count': item['count']} 
                for item in bookings_per_day
            ]
        }
        
        return Response(data)


class BookingMetricsView(views.APIView):
    """
    View to return detailed booking metrics for admin users
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Time periods for analysis
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        this_week_start = today - timedelta(days=now.weekday())
        last_week_start = this_week_start - timedelta(days=7)
        this_month_start = today.replace(day=1)
        
        # Get bookings for each time period
        bookings_today = Booking.objects.filter(created_at__gte=today).count()
        bookings_yesterday = Booking.objects.filter(
            created_at__gte=yesterday, 
            created_at__lt=today
        ).count()
        
        bookings_this_week = Booking.objects.filter(
            created_at__gte=this_week_start
        ).count()
        
        bookings_last_week = Booking.objects.filter(
            created_at__gte=last_week_start,
            created_at__lt=this_week_start
        ).count()
        
        bookings_this_month = Booking.objects.filter(
            created_at__gte=this_month_start
        ).count()
        
        # Calculate growth rates
        week_growth_rate = (
            ((bookings_this_week - bookings_last_week) / max(bookings_last_week, 1)) * 100
            if bookings_last_week > 0 else 100
        )
        
        day_growth_rate = (
            ((bookings_today - bookings_yesterday) / max(bookings_yesterday, 1)) * 100
            if bookings_yesterday > 0 else 100
        )
        
        # Format the response data
        data = {
            'bookings_count': {
                'today': bookings_today,
                'yesterday': bookings_yesterday,
                'this_week': bookings_this_week,
                'last_week': bookings_last_week,
                'this_month': bookings_this_month,
            },
            'growth_rates': {
                'daily': round(day_growth_rate, 2),
                'weekly': round(week_growth_rate, 2),
            }
        }
        
        return Response(data)
