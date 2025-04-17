# config/microsoft_calendar.py
import msal

def get_microsoft_calendar_service(token):
    app = msal.PublicClientApplication(
        "YOUR_CLIENT_ID", authority="https://login.microsoftonline.com/YOUR_TENANT_ID"
    )
    result = app.acquire_token_by_refresh_token(token)
    return result
