from .exporters.csv_exporter import export_booking_history_csv
from .models import ReportRequest

def generate_report(report: ReportRequest):
    if report.report_type == 'history':
        file_url = export_booking_history_csv(report.user)
        report.file_link = file_url
        report.status = 'completed'
        report.save()
