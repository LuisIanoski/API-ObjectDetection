from django.db import models
from camera.models import Camera

class Dashboard(models.Model):
    RISK_CHOICES = [
        ('baixo', 'Baixo'),
        ('medio', 'Médio'),
        ('alto', 'Alto'),
        ('critico', 'Crítico'),
    ]
    
    dashboard_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    cameras = models.ManyToManyField(Camera, related_name='dashboards')
    risco = models.CharField(
        max_length=20,
        choices=RISK_CHOICES,
        default='baixo',
        verbose_name='Nível de Risco'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.dashboard_id}) - Risco: {self.get_risco_display()}"

    def get_risk_color(self):
        """Retorna a cor correspondente ao nível de risco"""
        colors = {
            'baixo': '#10b981',    # Verde
            'medio': '#f59e0b',    # Amarelo
            'alto': '#ef4444',     # Vermelho
            'critico': '#dc2626',  # Vermelho escuro
        }
        return colors.get(self.risco, '#6b7280')  # Cinza padrão

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'