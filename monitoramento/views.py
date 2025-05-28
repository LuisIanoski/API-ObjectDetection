from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse, HttpResponse
import cv2
import threading
import time
from .camera import Camera

class CameraDetectionsView(APIView):
    def get(self, request, camera_id=None):
        if camera_id:
            # Lógica existente para câmera específica
            camera = Camera(camera_id=camera_id, url="http://192.168.3.7:8080/video")
            date = request.query_params.get("date")
            detections = camera.get_detections(date=date)
            return Response(detections, status=status.HTTP_200_OK)
        else:
            # Página inicial
            return Response({
                "message": "API de Monitoramento de Câmeras",
                "endpoints": {
                    "stream": "/api/cameras/CAM001/stream/",
                    "detections": "/api/cameras/CAM001/detections/"
                }
            })

class CameraStreamView(APIView):
    def get(self, request, camera_id):
        try:
            camera = Camera(camera_id=camera_id, url="http://192.168.3.7:8080/video")
            return StreamingHttpResponse(
                camera.generate_frames(),
                content_type='multipart/x-mixed-replace; boundary=frame'
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
