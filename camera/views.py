from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Camera
from .serializers import CameraSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

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

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def camera_status(request, camera_id):
    try:
        camera = Camera.objects.get(camera_id=camera_id)
        return Response({
            'camera_status': camera.camera_status,
            'last_updated': camera.updated_at
        })
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=404)