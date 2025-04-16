from rest_framework import serializers
from .models import User, Department
from django.contrib.auth.password_validation import validate_password

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ['password']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'role', 'department']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
