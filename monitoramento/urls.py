from django.urls import path
from .views import DetectionView, CameraStreamView

urlpatterns = [
    path('detections/', DetectionView.as_view()),
    path('cameras/<str:camera_id>/detections/', DetectionView.as_view()),
    path('cameras/<str:camera_id>/stream/', CameraStreamView.as_view()),
]