# middleware.py
import pytz
from django.utils import timezone
from django.utils.translation import activate
from .models import UserTimezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user's timezone or use default UTC
        user = request.user
        if user.is_authenticated:
            try:
                user_timezone = UserTimezone.objects.get(user=user)
                timezone.activate(pytz.timezone(user_timezone.timezone))
            except UserTimezone.DoesNotExist:
                timezone.activate(pytz.utc)
        else:
            timezone.activate(pytz.utc)

        # Set the language from the request (use URL or headers for language selection)
        language_code = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en').split(',')[0]
        activate(language_code)

        response = self.get_response(request)
        return response
