# utils.py
from django.utils import timezone
from datetime import datetime
import pytz

def convert_to_timezone(dt, timezone_str):
    tz = pytz.timezone(timezone_str)
    return dt.astimezone(tz)

def get_current_time_in_timezone(timezone_str):
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz)
