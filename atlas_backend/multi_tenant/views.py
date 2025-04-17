# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Tenant

def tenant_dashboard(request):
    tenant = request.tenant
    branding = {
        "logo": tenant.logo.url if tenant.logo else None,
        "primary_color": tenant.colors.get('primary', '#000000')
    }
    return render(request, 'tenant_dashboard.html', {'tenant': tenant, 'branding': branding})

def update_tenant_logo(request):
    tenant = request.tenant
    if request.method == 'POST' and request.FILES.get('logo'):
        tenant.logo = request.FILES['logo']
        tenant.save()
        return JsonResponse({"message": "Logo updated successfully!"})
    return JsonResponse({"error": "No logo file provided."})
