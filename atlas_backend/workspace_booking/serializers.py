from rest_framework import serializers
from .models import Booking, Room, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'room_id', 'start_time', 'end_time', 'title', 'is_recurring', 'notes']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        # Conflict detection logic
        room = validated_data['room']
        start = validated_data['start_time']
        end = validated_data['end_time']

        if Booking.objects.filter(room=room, start_time__lt=end, end_time__gt=start).exists():
            raise serializers.ValidationError("This booking overlaps with an existing booking.")

        return super().create(validated_data)
