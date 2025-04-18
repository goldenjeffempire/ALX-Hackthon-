# multi_tenant/models.py

from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Workspace(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='workspaces')
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class TenantSettings(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='settings')
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f"{self.tenant.name} Settings"
