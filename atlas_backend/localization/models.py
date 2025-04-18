# localization/models.py
from django.db import models
from django.conf import settings
import pytz

class UserTimezone(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_timezone')
    timezone = models.CharField(
        max_length=225,
        choices=[(tz, tz) for tz in pytz.all_timezones],
        default='UTC'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Time Zone"

