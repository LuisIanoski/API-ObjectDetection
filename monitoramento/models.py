from django.db import models
from camera.models import Camera

class Detection(models.Model):
    detection_id = models.AutoField(primary_key=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='detections')
    detection_date = models.DateField()
    detection_time = models.TimeField()
    detections = models.JSONField()  # Stores the detection array
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'detections'
        ordering = ['-detection_date', '-detection_time']
