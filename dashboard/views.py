from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Dashboard
from .serializers import DashboardSerializer, DashboardCameraSerializer
from django.views.generic import TemplateView
from django.utils import timezone

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
                'dashboard_risco': dashboard.risco,
                'dashboard_risco_display': dashboard.get_risco_display(),
                'dashboard_risco_color': dashboard.get_risk_color(),
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
                'can_add_camera': False,
                'dashboard_risco': 'baixo',
                'dashboard_risco_display': 'Baixo',
                'dashboard_risco_color': '#10b981'
            })
            
        return context


class RiskManagementView(TemplateView):
    """View específica para a página de gerenciamento de risco"""
    template_name = 'risco.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_id = self.kwargs.get('dashboard_id')
        
        try:
            dashboard = Dashboard.objects.get(dashboard_id=dashboard_id)
            cameras = dashboard.cameras.all()
            
            context.update({
                'dashboard_id': dashboard_id,
                'dashboard_name': dashboard.name,
                'dashboard_risco': dashboard.risco,
                'dashboard_risco_display': dashboard.get_risco_display(),
                'dashboard_risco_color': dashboard.get_risk_color(),
                'dashboard_created': dashboard.created_at,
                'dashboard_updated': dashboard.updated_at,
                'risk_priority': dashboard.get_risk_priority(),
                'risk_description': dashboard.get_risk_description(),
                'can_upgrade_risk': dashboard.can_upgrade_risk(),
                'can_downgrade_risk': dashboard.can_downgrade_risk(),
                'next_risk_level': dashboard.get_next_risk_level(),
                'previous_risk_level': dashboard.get_previous_risk_level(),
                'is_high_risk': dashboard.is_high_risk(),
                'cameras': [{
                    'id': camera.camera_id,
                    'location': camera.camera_loc,
                    'status': camera.camera_status,
                    'link': camera.camera_link,
                } for camera in cameras],
                'cameras_count': cameras.count(),
                'error': None
            })
        except Dashboard.DoesNotExist:
            context.update({
                'dashboard_id': dashboard_id,
                'error': 'Dashboard não encontrado',
                'cameras': [],
                'cameras_count': 0,
                'dashboard_risco': 'baixo',
                'dashboard_risco_display': 'Baixo',
                'dashboard_risco_color': '#10b981',
                'risk_priority': 1,
                'risk_description': 'Dashboard não encontrado',
                'can_upgrade_risk': False,
                'can_downgrade_risk': False,
                'next_risk_level': None,
                'previous_risk_level': None,
                'is_high_risk': False
            })
            
        return context

class DashboardViewSet(viewsets.ModelViewSet):
    """ViewSet completo para gerenciamento de dashboards com manipulação de risco"""
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    lookup_field = 'dashboard_id'
    permission_classes = [AllowAny]

    @action(detail=True, methods=['patch'], url_path='update-risk')
    def update_risk(self, request, dashboard_id=None):
        """Endpoint específico para atualizar o nível de risco"""
        try:
            dashboard = self.get_object()
            new_risk = request.data.get('risco')
            
            if new_risk not in dict(Dashboard.RISK_CHOICES):
                return Response(
                    {'error': f'Nível de risco inválido. Opções: {[choice[0] for choice in Dashboard.RISK_CHOICES]}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            old_risk = dashboard.risco
            dashboard.risco = new_risk
            dashboard.save()
            
            return Response({
                'success': True,
                'message': f'Nível de risco alterado de "{dashboard.get_risco_display_for_value(old_risk)}" para "{dashboard.get_risco_display()}"',
                'dashboard_id': dashboard.dashboard_id,
                'old_risk': old_risk,
                'new_risk': new_risk,
                'new_risk_display': dashboard.get_risco_display(),
                'new_risk_color': dashboard.get_risk_color(),
                'updated_at': dashboard.updated_at
            })
            
        except Dashboard.DoesNotExist:
            return Response(
                {'error': 'Dashboard não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro interno: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'], url_path='risk-history')
    def risk_history(self, request, dashboard_id=None):
        """Endpoint para obter histórico de alterações de risco (futura implementação)"""
        try:
            dashboard = self.get_object()
            # Por enquanto retorna apenas o status atual
            # Em implementações futuras, pode integrar com um modelo de log
            return Response({
                'dashboard_id': dashboard.dashboard_id,
                'current_risk': dashboard.risco,
                'current_risk_display': dashboard.get_risco_display(),
                'current_risk_color': dashboard.get_risk_color(),
                'last_updated': dashboard.updated_at,
                'message': 'Histórico de risco será implementado em versão futura'
            })
        except Dashboard.DoesNotExist:
            return Response(
                {'error': 'Dashboard não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='risk-levels')
    def risk_levels(self, request):
        """Endpoint para listar todos os níveis de risco disponíveis"""
        risk_levels = [
            {
                'value': choice[0],
                'display': choice[1],
                'color': Dashboard().get_risk_color_for_value(choice[0])
            }
            for choice in Dashboard.RISK_CHOICES
        ]
        
        return Response({
            'risk_levels': risk_levels,
            'total_levels': len(risk_levels)
        })

# Manter as views de função existentes para compatibilidade
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

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
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
    
    elif request.method == 'PATCH':
        # Permite atualizações parciais, incluindo apenas risco
        serializer = DashboardSerializer(dashboard, data=request.data, partial=True)
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