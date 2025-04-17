# tests/test_integration.py
from rest_framework.test import APITestCase
from rest_framework import status

class IntegrationTests(APITestCase):
    def test_google_calendar_sync(self):
        response = self.client.post('/api/google_calendar_sync/', {
            'google_token': 'dummy_token',
            'calendar_id': 'primary'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Google Calendar Sync Started!')
