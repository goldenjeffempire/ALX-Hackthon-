# tests/test_tenant.py
from django.test import TestCase
from multi_tenant.models import Tenant
from django.contrib.auth.models import User

class TenantTestCase(TestCase):
    def test_create_tenant(self):
        tenant = Tenant.objects.create(
            name="Test Tenant",
            domain_url="testtenant.com"
        )
        self.assertEqual(tenant.name, "Test Tenant")
        self.assertEqual(tenant.domain_url, "testtenant.com")
    
    def test_tenant_logo_update(self):
        tenant = Tenant.objects.create(
            name="Test Tenant",
            domain_url="testtenant.com"
        )
        tenant.logo = 'path_to_logo.jpg'
        tenant.save()
        self.assertEqual(tenant.logo.url, 'path_to_logo.jpg')
