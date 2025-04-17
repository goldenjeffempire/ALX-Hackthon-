# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GoogleCalendarIntegration
from .tasks import sync_google_calendar

class GoogleCalendarSync(APIView):
    def post(self, request):
        user = request.user
        google_token = request.data.get('google_token')
        calendar_id = request.data.get('calendar_id')

        # Save the Google Calendar integration
        GoogleCalendarIntegration.objects.update_or_create(
            user=user,
            google_token=google_token,
            calendar_id=calendar_id
        )

        # Start an asynchronous task to sync calendar
        sync_google_calendar.delay()

        return Response({"message": "Google Calendar Sync Started!"}, status=200)
