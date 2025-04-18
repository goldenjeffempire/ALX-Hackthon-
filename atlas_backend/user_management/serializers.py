from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, Location
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# User Serializer for listing users and handling authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')

# UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'phone_number', 'profile_picture', 'location')

# Register User Serializer (for creating a new user)
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password')

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Login User Serializer (for JWT authentication)
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = None
        try:
            user = get_user_model().objects.get(email=data['email'])
            if not user.check_password(data['password']):
                raise serializers.ValidationError("Incorrect password")
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")

        return {'user': user}
