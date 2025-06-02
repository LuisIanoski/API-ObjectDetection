from rest_framework import serializers
from .models import Camera

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['camera_id', 'camera_link', 'camera_status', 'camera_loc']
        lookup_field = 'camera_id'