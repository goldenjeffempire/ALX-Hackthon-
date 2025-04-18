# multi_tenant/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tenant, Workspace, TenantSettings
from .serializers import TenantSerializer, WorkspaceSerializer, TenantSettingsSerializer
from rest_framework.permissions import IsAuthenticated

class TenantView(APIView):
    def get(self, request):
        tenants = Tenant.objects.all()
        return Response(TenantSerializer(tenants, many=True).data)

    def post(self, request):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class WorkspaceView(APIView):
    def get(self, request, tenant_id):
        workspaces = Workspace.objects.filter(tenant_id=tenant_id)
        return Response(WorkspaceSerializer(workspaces, many=True).data)

    def post(self, request, tenant_id):
        serializer = WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_id=tenant_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TenantSettingsView(APIView):
    def get(self, request, tenant_id):
        try:
            settings = TenantSettings.objects.get(tenant_id=tenant_id)
            return Response(TenantSettingsSerializer(settings).data)
        except TenantSettings.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

    def patch(self, request, tenant_id):
        try:
            settings = TenantSettings.objects.get(tenant_id=tenant_id)
            serializer = TenantSettingsSerializer(settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except TenantSettings.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
