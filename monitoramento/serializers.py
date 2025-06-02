from rest_framework import serializers
from .models import Detection

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ['detection_id', 'camera', 'detection_date', 
                 'detection_time', 'detections']