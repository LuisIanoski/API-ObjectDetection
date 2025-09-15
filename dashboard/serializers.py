from rest_framework import serializers
from .models import Dashboard
from camera.models import Camera

class DashboardCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = [
            'camera_id',
            'camera_link',
            'camera_status',
            'camera_loc'
        ]
        extra_kwargs = {
            'camera_id': {'required': True},
            'camera_link': {'required': True},
            'camera_status': {'required': True},
            'camera_loc': {'required': True}
        }

class DashboardSerializer(serializers.ModelSerializer):
    cameras = DashboardCameraSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = ['dashboard_id', 'name', 'cameras', 'created_at']