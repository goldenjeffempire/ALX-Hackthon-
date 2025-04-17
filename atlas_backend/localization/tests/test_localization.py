# tests/test_localization.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from multi_tenant.models import Tenant
from localization.models import UserTimezone

class LocalizationTestCase(TestCase):
    def test_timezone_update(self):
        user = User.objects.create_user(username='testuser', password='password')
        tenant = Tenant.objects.create(name='Test Tenant', domain_url='testtenant.com')
        user_timezone = UserTimezone.objects.create(user=user, timezone='America/New_York')

        self.client.login(username='testuser', password='password')

        # Test timezone update
        response = self.client.post('/update_timezone/', {'timezone': 'Asia/Kolkata'})
        self.assertEqual(response.status_code, 302)
        user_timezone.refresh_from_db()
        self.assertEqual(user_timezone.timezone, 'Asia/Kolkata')

    def test_language_update(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Test language update
        response = self.client.post('/update_language/', {'language': 'fr'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['django_language'], 'fr')
