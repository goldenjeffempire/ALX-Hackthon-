from django.core.mail import send_mail

def notify_maintenance_team(request_obj):
    send_mail(
        subject=f"New Maintenance Request: {request_obj.title}",
        message=f"Priority: {request_obj.priority}\nDescription: {request_obj.description}",
        from_email='noreply@atlas.com',
        recipient_list=['maintenance@atlas.com']
    )
