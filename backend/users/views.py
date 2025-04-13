from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Role
from .serializers import (
    UserSerializer, UserRegisterSerializer, UserUpdateSerializer,
    ChangePasswordSerializer, RoleSerializer
)
from .permissions import IsAdminOrSelf, IsAdminOrReadOnly

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    filterset_fields = ['role', 'department', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'department', 'job_title']

    def get_permissions(self):
        """
        Override permissions based on action:
        - Only admins can list all users or create new ones
        - Users can view and update their own profiles
        """
        if self.action in ['create', 'list', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        """
        Use appropriate serializer based on the action
        """
        if self.action == 'create':
            return UserRegisterSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        if self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrSelf])
    def change_password(self, request, pk=None):
        """
        Change password endpoint
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Wrong password."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def toggle_two_factor(self, request, pk=None):
        """
        Toggle two-factor authentication
        """
        user = self.get_object()
        user.two_factor_enabled = not user.two_factor_enabled
        user.save()

        return Response({
            "message": f"Two-factor authentication {'enabled' if user.two_factor_enabled else 'disabled'}",
            "two_factor_enabled": user.two_factor_enabled
        })

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's profile
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing custom roles.
    Only admins can create, update, and delete roles.
    """
    queryset = Role.objects.all().order_by('name')
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['name', 'description']
