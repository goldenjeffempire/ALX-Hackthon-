from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from workspaces.models import Workspace, WorkspaceType
from ..models import Booking


User = get_user_model()

class BookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        
        self.workspace_type = WorkspaceType.objects.create(
            name='Meeting Room',
            description='Test description'
        )
        
        self.workspace = Workspace.objects.create(
            name='Test Workspace',
            description='Test description',
            opening_time=timezone.now().time().replace(hour=9, minute=0),  # 9AM
            closing_time=timezone.now().time().replace(hour=17, minute=0), # 5PM
            max_capacity=10,
            min_capacity=1,
            workspace_type=self.workspace_type,
            price_per_hour=25.00
        )
        
        self.valid_start = timezone.now() + timedelta(days=1)
        self.valid_end = self.valid_start + timedelta(hours=2)

    def test_create_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=self.valid_start,
            end_time=self.valid_end
        )
        self.assertEqual(booking.status, Booking.Status.PENDING)
        self.assertEqual(booking.user, self.user)
        
    def test_time_validation(self):
        # End before start
        with self.assertRaises(ValidationError):
            Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=self.valid_start,
                end_time=self.valid_start - timedelta(hours=1)
            ).full_clean()
        
        # Outside workspace hours
        early_start = self.valid_start.replace(hour=8, minute=0)  # 8AM
        with self.assertRaises(ValidationError):
            Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=early_start,
                end_time=early_start + timedelta(hours=1)
            ).full_clean()
    
    def test_overlap_validation(self):
        # Create initial booking
        Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=self.valid_start,
            end_time=self.valid_end
        )
        
        # Try overlapping booking
        with self.assertRaises(ValidationError):
            Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=self.valid_start + timedelta(minutes=30),
                end_time=self.valid_end + timedelta(minutes=30)
                    ).full_clean()
