# multi_tenant/urls.py

from django.urls import path
from .views import TenantView, WorkspaceView, TenantSettingsView

urlpatterns = [
    path('tenants/', TenantView.as_view(), name='tenant-list'),
    path('tenants/<int:tenant_id>/workspaces/', WorkspaceView.as_view(), name='tenant-workspaces'),
    path('tenants/<int:tenant_id>/settings/', TenantSettingsView.as_view(), name='tenant-settings'),
]
