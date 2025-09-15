from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Dashboard
from .serializers import DashboardSerializer, DashboardCameraSerializer
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_id = self.kwargs.get('dashboard_id')
        
        try:
            dashboard = Dashboard.objects.get(dashboard_id=dashboard_id)
            cameras = dashboard.cameras.all()
            
            context.update({
                'dashboard_id': dashboard_id,
                'dashboard_name': dashboard.name,
                'dashboard_created': dashboard.created_at,
                'dashboard_updated': dashboard.updated_at,
                'cameras': [{
                    'id': camera.camera_id,
                    'location': camera.camera_loc,
                    'status': camera.camera_status,
                    'link': camera.camera_link,
                } for camera in cameras],
                'cameras_count': cameras.count(),
                'can_add_camera': cameras.count() < 3,
                'error': None
            })
        except Dashboard.DoesNotExist:
            context.update({
                'dashboard_id': dashboard_id,
                'error': 'Dashboard não encontrado',
                'cameras': [],
                'cameras_count': 0,
                'can_add_camera': False
            })
            
        return context

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def create_dashboard(request):
    if request.method == 'GET':
        dashboards = Dashboard.objects.all()
        serializer = DashboardSerializer(dashboards, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DashboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
@authentication_classes([])
def dashboard_detail(request, dashboard_id):
    try:
        dashboard = Dashboard.objects.get(dashboard_id=dashboard_id)
    except Dashboard.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DashboardSerializer(dashboard)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DashboardSerializer(dashboard, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dashboard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def add_camera_to_dashboard(request, dashboard_id):
    try:
        dashboard = Dashboard.objects.get(dashboard_id=dashboard_id)
        
        if dashboard.cameras.count() >= 3:
            return Response(
                {'error': 'Dashboard already has 3 cameras (maximum allowed)'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DashboardCameraSerializer(data=request.data)
        if serializer.is_valid():
            camera = serializer.save()
            dashboard.cameras.add(camera)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Dashboard.DoesNotExist:
        return Response(
            {'error': 'Dashboard not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
