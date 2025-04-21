from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
import logging

from bookings.models import Booking

# Set up logger
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Booking)
def validate_booking_times(sender, instance, **kwargs):
    """
    Validate that the booking end time is after the start time
    """
    if instance.end_time <= instance.start_time:
        raise ValueError("Booking end time must be after start time")

@receiver(post_save, sender=Booking)
def handle_booking_status_change(sender, instance, created, **kwargs):
    """
    Signal handler for booking status changes
    """
    # Import here to avoid circular import
    from notifications.services import (
        notify_booking_created,
        notify_booking_confirmed,
        notify_booking_cancelled,
        notify_booking_updated,
        notify_booking_reminder
    )
    
    # Track old status for status change detection
    old_status = getattr(instance, '_old_status', None)
    current_status = instance.status
    
    try:
        if created:
            # Send notification for a new booking
            logger.info(f"New booking created: {instance.id}")
            notify_booking_created(instance)
        
        # Handle status changes for existing bookings
        elif not created and old_status and old_status != current_status:
            logger.info(f"Booking status changed from {old_status} to {current_status}: {instance.id}")
            
            if current_status == 'confirmed':
                notify_booking_confirmed(instance)
            
            elif current_status == 'cancelled':
                notify_booking_cancelled(instance)
            
            elif current_status == 'completed':
                # You could add a completion notification if needed
                pass
            
            else:
                # For other status changes, send a generic update
                notify_booking_updated(instance)
                
        # For updates without status changes
        elif not created and not old_status:
            logger.info(f"Booking updated: {instance.id}")
            notify_booking_updated(instance)
            
    except Exception as e:
        logger.error(f"Failed to send booking notification: {str(e)}")
    
    # Check if booking needs to be marked as completed automatically
    if instance.status != 'completed' and instance.end_time < timezone.now():
        logger.info(f"Auto-completing past booking: {instance.id}")
        instance.status = 'completed'
        
        # Disable signals temporarily to avoid infinite loop
        post_save.disconnect(handle_booking_status_change, sender=Booking)
        instance.save()
        post_save.connect(handle_booking_status_change, sender=Booking)
