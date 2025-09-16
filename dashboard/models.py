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
        """Retorna a cor correspondente ao nível de risco atual"""
        return self.get_risk_color_for_value(self.risco)
    
    def get_risk_color_for_value(self, risk_value):
        """Retorna a cor correspondente a um valor específico de risco"""
        colors = {
            'baixo': '#10b981',    # Verde
            'medio': '#f59e0b',    # Amarelo
            'alto': '#ef4444',     # Vermelho
            'critico': '#dc2626',  # Vermelho escuro
        }
        return colors.get(risk_value, '#6b7280')  # Cinza padrão
    
    def get_risco_display_for_value(self, risk_value):
        """Retorna o display name para um valor específico de risco"""
        risk_dict = dict(self.RISK_CHOICES)
        return risk_dict.get(risk_value, 'Desconhecido')
    
    def get_risk_priority(self):
        """Retorna prioridade numérica do risco (para ordenação)"""
        priority_map = {
            'baixo': 1,
            'medio': 2,
            'alto': 3,
            'critico': 4,
        }
        return priority_map.get(self.risco, 0)
    
    def is_high_risk(self):
        """Verifica se o dashboard está em nível de risco alto ou crítico"""
        return self.risco in ['alto', 'critico']
    
    def can_upgrade_risk(self):
        """Verifica se é possível aumentar o nível de risco"""
        return self.risco != 'critico'
    
    def can_downgrade_risk(self):
        """Verifica se é possível diminuir o nível de risco"""
        return self.risco != 'baixo'
    
    def get_next_risk_level(self):
        """Retorna o próximo nível de risco (escalação)"""
        risk_progression = ['baixo', 'medio', 'alto', 'critico']
        try:
            current_index = risk_progression.index(self.risco)
            if current_index < len(risk_progression) - 1:
                return risk_progression[current_index + 1]
        except ValueError:
            pass
        return None
    
    def get_previous_risk_level(self):
        """Retorna o nível de risco anterior (de-escalação)"""
        risk_progression = ['baixo', 'medio', 'alto', 'critico']
        try:
            current_index = risk_progression.index(self.risco)
            if current_index > 0:
                return risk_progression[current_index - 1]
        except ValueError:
            pass
        return None
    
    def get_risk_description(self):
        """Retorna uma descrição detalhada do nível de risco"""
        descriptions = {
            'baixo': 'Situação normal, monitoramento de rotina',
            'medio': 'Atenção necessária, monitoramento aumentado',
            'alto': 'Situação de alerta, ação imediata recomendada',
            'critico': 'Perigo iminente, ação urgente necessária'
        }
        return descriptions.get(self.risco, 'Nível de risco não definido')

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['-updated_at']  # Ordenar por mais recentemente atualizado