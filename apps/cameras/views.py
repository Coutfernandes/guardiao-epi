from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Camera
from .serializers import CameraSerializer


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