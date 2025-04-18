# Generated by Django 4.2.20 on 2025-04-18 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('room_type', models.CharField(choices=[('boardroom', 'Boardroom'), ('classroom', 'Classroom'), ('private_office', 'Private Office'), ('hot_desk', 'Hot Desk')], max_length=50)),
                ('capacity', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='workspace_booking.location')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('is_recurring', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace_booking.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['start_time'],
                'unique_together': {('room', 'start_time', 'end_time')},
            },
        ),
    ]
