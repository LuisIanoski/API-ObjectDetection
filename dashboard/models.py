from django.db import models
from camera.models import Camera

# Create your models here.

class Dashboard(models.Model):
    dashboard_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    cameras = models.ManyToManyField(Camera, related_name='dashboards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.dashboard_id})"

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
