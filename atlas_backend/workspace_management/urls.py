from django.urls import path
from .views import FloorPlanListCreateView, WorkspaceListCreateView, WorkspaceDetailView

urlpatterns = [
    path('floor-plans/', FloorPlanListCreateView.as_view(), name='floorplan-list'),
    path('workspaces/', WorkspaceListCreateView.as_view(), name='workspace-list'),
    path('workspaces/<int:pk>/', WorkspaceDetailView.as_view(), name='workspace-detail'),
]
