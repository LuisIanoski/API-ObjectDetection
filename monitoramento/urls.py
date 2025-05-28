from django.urls import path
from .views import CameraDetectionsView, CameraStreamView

urlpatterns = [
    # Adicione uma view inicial
    path('', CameraDetectionsView.as_view(), name='api-root'),
    path('cameras/<str:camera_id>/detections/', CameraDetectionsView.as_view(), name='camera-detections'),
    path('cameras/<str:camera_id>/stream/', CameraStreamView.as_view(), name='camera-stream'),
]