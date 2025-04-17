# models.py
from django.db import models
from django_tenants.models import TenantMixin

class Tenant(TenantMixin):
    name = models.CharField(max_length=255)
    domain_url = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)
    colors = models.JSONField(default=dict)  # To store tenant-specific branding (e.g., primary color)

    auto_create_schema = True  # Automatically create the schema for each tenant
