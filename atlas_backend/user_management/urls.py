from django.urls import path
from .views import RegisterView, ProfileView, DepartmentListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('departments/', DepartmentListView.as_view(), name='departments'),
]
