from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Camera
from .serializers import CameraSerializer
from .services import verificar_camera, verificar_todas_cameras


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        camera = self.get_object()
        novo_status = request.data.get('status')
        if novo_status not in ['online', 'offline', 'alerta']:
            return Response(
                {'erro': 'Status invalido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        camera.status = novo_status
        camera.save()
        return Response(CameraSerializer(camera).data)

    @action(detail=True, methods=['post'])
    def verificar(self, request, pk=None):
        camera = self.get_object()
        verificar_camera(camera.id)
        camera.refresh_from_db()
        return Response(CameraSerializer(camera).data)

    @action(detail=False, methods=['post'])
    def verificar_todas(self, request):
        verificar_todas_cameras()
        cameras = Camera.objects.all()
        return Response(CameraSerializer(cameras, many=True).data)