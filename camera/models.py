from django.db import models

class Camera(models.Model):
    camera_id = models.CharField(max_length=50, unique=True)
    camera_link = models.URLField()
    camera_status = models.CharField(max_length=100, default='active')
    camera_loc = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Camera {self.camera_id} - {self.camera_loc}"

    class Meta:
        db_table = 'cameras'
