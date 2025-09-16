"""
URL configuration for extracaoimg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from dashboard.views import DashboardView, RiskManagementView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/', include('camera.urls')),
    path('api/', include('monitoramento.urls')),
    path('api/dashboards/', include('dashboard.urls', namespace='dashboard')),
    path('api-auth/', include('rest_framework.urls')),
    
    # Dashboard Management Pages
    path('manage/', TemplateView.as_view(template_name='dashboard_management.html'), name='dashboard-management'),
    
    # Dashboard Views
    path('dashboard/<str:dashboard_id>/', DashboardView.as_view(), name='dashboard-view'),
    path('dashboard/<str:dashboard_id>/risco/', RiskManagementView.as_view(), name='risk-management'),
    
    # Redirects e páginas auxiliares
    path('risco/<str:dashboard_id>/', RiskManagementView.as_view(), name='risk-management-short'),
]

# Comentários sobre as rotas:
# 
# Dashboard Principal:
# /dashboard/{dashboard_id}/                   - Dashboard completo com vídeo e monitoramento
# 
# Gerenciamento de Risco:
# /dashboard/{dashboard_id}/risco/             - Página dedicada ao gerenciamento de risco
# /risco/{dashboard_id}/                       - Atalho para gerenciamento de risco
# 
# API Endpoints (via dashboard.urls):
# /api/dashboards/                             - CRUD de dashboards
# /api/dashboards/{id}/update-risk/            - Atualização de risco
# /api/dashboards/{id}/risk-history/           - Histórico de risco
# /api/dashboards/risk-levels/                 - Níveis de risco disponíveis
# 
# Exemplos de uso:
# - Dashboard principal: /dashboard/sala-controle/
# - Gerenciar risco: /dashboard/sala-controle/risco/
# - Atalho para risco: /risco/sala-controle/