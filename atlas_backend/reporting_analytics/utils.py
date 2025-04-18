from .exporters.csv_exporter import export_booking_history_csv
from .models import ReportRequest

def generate_report(report: ReportRequest):
    """
    Generates a CSV report based on the report request.
    Currently supports 'history' type.
    """
    if report.report_type == 'history':
        # Fetch actual user data from the database
        bookings = Booking.objects.filter(user=report.user).values(
            'user__username', 'date', 'amount'
        )

        # Convert queryset to list of dictionaries
        data = list(bookings)

        # Generate the CSV
        file_url = export_booking_history_csv(data)

        # Update the report record
        report.file_link = file_url
        report.status = 'completed'
        report.save()
    else:
        report.status = 'failed'
        report.save()
