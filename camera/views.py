from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Camera
from .serializers import CameraSerializer

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit.
    """
    def has_permission(self, request, view):
        # Allow GET requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Require admin for POST/PUT/DELETE
        return request.user and request.user.is_staff

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    lookup_field = 'camera_id'
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object(self):
        camera_id = self.kwargs.get('camera_id')
        return Camera.objects.get(camera_id=camera_id)

    def destroy(self, request, *args, **kwargs):
        camera = self.get_object()
        camera.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        camera = self.get_object()
        serializer = self.get_serializer(camera, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)