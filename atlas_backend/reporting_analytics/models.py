from django.db import models
from django.conf import settings

class ReportRequest(models.Model):
    REPORT_TYPES = [
        ('usage', 'Usage Report'),
        ('history', 'Booking History'),
        ('custom', 'Custom Query'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, default='processing')

    def __str__(self):
        return f"{self.report_type} by {self.user.email} on {self.generated_at}"
