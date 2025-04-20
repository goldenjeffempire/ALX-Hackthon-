from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    UserProfileView,
    UserDetailView,
    CheckAuthView
)

app_name = 'accounts'

urlpatterns = [
    # JWT token endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
    path('check-auth/', CheckAuthView.as_view(), name='check_auth'),
    
    # User detail endpoint - admin only for modification
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]
