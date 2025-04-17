# urls.py
from django.urls import path
from .views import tenant_dashboard, update_tenant_logo

urlpatterns = [
    path('dashboard/', tenant_dashboard, name='tenant_dashboard'),
    path('update_logo/', update_tenant_logo, name='update_logo'),
]
