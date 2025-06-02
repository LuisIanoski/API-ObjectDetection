from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from camera.services import CameraService
from .models import Detection
from .serializers import DetectionSerializer
from datetime import datetime

class CameraStreamView(APIView):
    def get(self, request, camera_id):
        try:
            camera_service = CameraService(camera_id)
            return StreamingHttpResponse(
                camera_service.generate_frames(),
                content_type='multipart/x-mixed-replace; boundary=frame'
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class DetectionView(APIView):
    def get(self, request, camera_id=None):
        date = request.query_params.get('date')
        queryset = Detection.objects.all()
        
        if camera_id:
            queryset = queryset.filter(camera__camera_id=camera_id)
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%d/%m/%y').date()
                queryset = queryset.filter(detection_date=date_obj)
            except ValueError:
                return Response({"error": "Invalid date format. Use DD/MM/YY"}, status=400)
                
        serializer = DetectionSerializer(queryset, many=True)
        return Response(serializer.data)
