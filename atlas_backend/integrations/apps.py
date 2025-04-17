from django.apps import AppConfig


class IntegrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integrations'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        from django_celery_beat.models import CrontabSchedule
        from django.utils.timezone import now
        import json

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1, period=IntervalSchedule.HOURS
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Sync Google Calendar',
            task='integrations.tasks.sync_google_calendar',
            defaults={'start_time': now(), 'args': json.dumps([])},
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Sync Microsoft Calendar',
            task='integrations.tasks.sync_microsoft_calendar',
            defaults={'start_time': now(), 'args': json.dumps([])},
        )
