# localization/models.py
from django.db import models
from django.conf import settings
import pytz

class UserTimezone(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- ✅ FIXED
    timezone = models.CharField(
        max_length=63,
        choices=[(tz, tz) for tz in pytz.all_timezones],
        default='UTC'
    )

    def __str__(self):
        return f"{self.user.username}'s timezone: {self.timezone}"
