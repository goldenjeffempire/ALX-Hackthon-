from django.urls import path, include
from .views import SignupAPIView, LoginAPIView

urlpatterns = [
    path('api/auth/signup', SignupAPIView.as_view(), name='signup'),
    path('api/auth/login', LoginAPIView.as_view(), name='login'),
    path('accounts/', include('allauth.urls')),
]
