from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that adds user information to the token response
    """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to token response
        user = self.user
        data.update({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin,
        })
        
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 
                  'first_name', 'last_name', 'is_admin', 'bio', 'phone_number']
        read_only_fields = ['id', 'is_admin']
        
    def validate(self, attrs):
        """
        Validate that passwords match
        """
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password fields don't match."})
        
        # Remove confirm_password from the attributes
        attrs.pop('confirm_password', None)
        return attrs
        
    def create(self, validated_data):
        """
        Create and return a new user with encrypted password
        """
        user = User.objects.create_user(
            username=validated_data.get('username', ''),
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        
        return user
    
    def update(self, instance, validated_data):
        """
        Update and return an existing user
        """
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (without sensitive data)
    """
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'full_name', 'bio', 'phone_number', 'is_admin']
        read_only_fields = ['id', 'email', 'is_admin']
