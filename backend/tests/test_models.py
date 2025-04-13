from django.test import TestCase
from django.contrib.auth.models import User
from booking.models import WorkspaceType, WorkspaceAmenity, Workspace, Booking, UserProfile, Notification
from django.utils import timezone
from datetime import timedelta

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.workspace_type = WorkspaceType.objects.create(name='Private Office')
        self.amenity = WorkspaceAmenity.objects.create(name='Wi-Fi')
        self.workspace = Workspace.objects.create(
            name='Test Workspace',
            description='A nice quiet room',
            location='Building A',
            capacity=5,
            available=True,
            workspace_type=self.workspace_type,
            created_by=self.user
        )
        self.workspace.amenities.add(self.amenity)

    def test_workspace_type_str(self):
        self.assertEqual(str(self.workspace_type), 'Private Office')

    def test_workspace_amenity_str(self):
        self.assertEqual(str(self.amenity), 'Wi-Fi')

    def test_workspace_str(self):
        self.assertEqual(str(self.workspace), 'Test Workspace')

    def test_booking_creation(self):
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=2)
        booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=start_time,
            end_time=end_time,
            status='pending'
        )
        self.assertEqual(str(booking), f'{self.user.username} - {self.workspace.name} ({start_time})')

    def test_user_profile_str(self):
        profile = UserProfile.objects.create(user=self.user, company_name='Test Company')
        self.assertEqual(str(profile), 'testuser')

    def test_notification_str(self):
        notification = Notification.objects.create(
            user=self.user,
            message='This is a test notification'
        )
        self.assertEqual(str(notification), f'Notification for {self.user.username}')
