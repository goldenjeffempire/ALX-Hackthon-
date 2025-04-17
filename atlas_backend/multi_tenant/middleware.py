# middleware.py
from django_tenants.middleware import TenantMiddleware as BaseTenantMiddleware

class TenantMiddleware(BaseTenantMiddleware):
    tenant_model = 'multi_tenant.Tenant'  # Use the Tenant model defined earlier
