# config/google_calendar.py
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_google_calendar_service(token):
    creds = Credentials.from_authorized_user_info(token)
    service = build('calendar', 'v3', credentials=creds)
    return service
