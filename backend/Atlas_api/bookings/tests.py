from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, date
from users.models import CustomUser
from .models import Workspace, Booking, Notification, WorkspaceUsageReport

class WorkspaceModelTest(TestCase):
    def setUp(self):
        self.workspace = Workspace.objects.create(
            name="Conference Room 1",
            space_type="meeting_room",
            capacity=10,
            description="Spacious room for meetings."
        )

    def test_workspace_creation(self):
        self.assertEqual(self.workspace.name, "Conference Room 1")
        self.assertEqual(self.workspace.get_space_type_display(), "Meeting Room")
        self.assertTrue(self.workspace.is_active)

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass")
        self.workspace = Workspace.objects.create(
            name="Desk 1",
            space_type="desk",
            capacity=1
        )
        self.start = timezone.now() + timedelta(hours=1)
        self.end = self.start + timedelta(hours=2)

    def test_valid_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=self.start,
            end_time=self.end
        )
        self.assertEqual(booking.status, 'confirmed')
        self.assertEqual(str(booking), f"{self.user.username} - {self.workspace.name} ({booking.start_time} to {booking.end_time})")

    def test_booking_time_constraint(self):
        with self.assertRaises(Exception):
            Booking.objects.create(
                user=self.user,
                workspace=self.workspace,
                start_time=self.end,
                end_time=self.start  # end < start, should raise IntegrityError due to check constraint
            )

    def test_is_active_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=timezone.now() - timedelta(minutes=30),
            end_time=timezone.now() + timedelta(minutes=30)
        )
        self.assertTrue(booking.is_active())

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="notifier", password="testpass")
        self.workspace = Workspace.objects.create(name="Desk 3", space_type="desk", capacity=1)
        self.booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2)
        )

    def test_notification_creation(self):
        notif = Notification.objects.create(
            user=self.user,
            booking=self.booking,
            message="Reminder: Your booking is coming up soon.",
            notification_type='reminder'
        )
        self.assertFalse(notif.is_read)
        self.assertEqual(str(notif), f"Reminder for {self.user.username}")

class WorkspaceUsageReportModelTest(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(username="admin", password="adminpass")
        self.report = WorkspaceUsageReport.objects.create(
            generated_by=self.admin,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            total_bookings=50,
            occupancy_rate=75.5,
            peak_usage_times={"10AM-12PM": 20, "2PM-4PM": 30}
        )

    def test_report_creation(self):
        self.assertEqual(self.report.total_bookings, 50)
        self.assertEqual(self.report.occupancy_rate, 75.5)
        self.assertIn("10AM-12PM", self.report.peak_usage_times)
        self.assertEqual(str(self.report), f"Usage Report {self.report.start_date} to {self.report.end_date}")
