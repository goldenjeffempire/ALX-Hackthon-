import csv
import os
from django.conf import settings
from workspace_booking.models import Booking
from django.utils.timezone import now

def export_booking_history_csv(user):
    filename = f"{user.id}_booking_history_{now().strftime('%Y%m%d%H%M')}.csv"
    filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Workspace', 'Start Time', 'End Time', 'Status'])

        bookings = Booking.objects.filter(user=user)
        for b in bookings:
            writer.writerow([b.workspace.name, b.start_time, b.end_time, b.status])

    return f"{settings.MEDIA_URL}reports/{filename}"
