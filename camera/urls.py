from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet

router = DefaultRouter()
router.register(r'cameras', CameraViewSet, basename='camera')

urlpatterns = router.urls