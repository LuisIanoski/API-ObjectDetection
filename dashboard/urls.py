from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.create_dashboard, name='create-dashboard'),  # New endpoint for dashboard creation
    path('<str:dashboard_id>/add-camera/', views.add_camera_to_dashboard, name='add-camera'),
]