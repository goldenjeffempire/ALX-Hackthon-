from rest_framework import generics, permissions
from .models import FloorPlan, Workspace
from .serializers import FloorPlanSerializer, WorkspaceSerializer

class FloorPlanListCreateView(generics.ListCreateAPIView):
    queryset = FloorPlan.objects.all()
    serializer_class = FloorPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.filter(is_active=True)
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkspaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]
