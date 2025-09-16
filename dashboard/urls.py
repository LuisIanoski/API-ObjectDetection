from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dashboard'

# Router para ViewSet
router = DefaultRouter()
router.register(r'', views.DashboardViewSet, basename='dashboard')

urlpatterns = [
    # ViewSet routes (inclui endpoints automáticos + custom actions)
    path('', include(router.urls)),
    
    # Endpoints específicos para compatibilidade (mantém os existentes)
    path('create/', views.create_dashboard, name='create-dashboard'),
    path('<str:dashboard_id>/detail/', views.dashboard_detail, name='dashboard-detail'),
    path('<str:dashboard_id>/add-camera/', views.add_camera_to_dashboard, name='add-camera'),
]

# Os seguintes endpoints são criados automaticamente pelo ViewSet:
# GET    /api/dashboards/                     - Lista todos os dashboards
# POST   /api/dashboards/                     - Cria novo dashboard
# GET    /api/dashboards/{id}/                - Detalhes de um dashboard
# PUT    /api/dashboards/{id}/                - Atualiza dashboard completo
# PATCH  /api/dashboards/{id}/                - Atualiza dashboard parcial
# DELETE /api/dashboards/{id}/                - Remove dashboard

# Endpoints customizados adicionados:
# PATCH  /api/dashboards/{id}/update-risk/    - Atualiza apenas o nível de risco
# GET    /api/dashboards/{id}/risk-history/   - Histórico de alterações de risco
# GET    /api/dashboards/risk-levels/         - Lista todos os níveis de risco disponíveis