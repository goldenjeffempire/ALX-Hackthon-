from django.contrib import admin
from .models import Booking, Room, Location

admin.site.register(Location)
admin.site.register(Room)
admin.site.register(Booking)
