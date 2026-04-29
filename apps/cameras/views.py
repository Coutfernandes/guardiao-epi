import cv2
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BaseAuthentication
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .models import Camera
from .serializers import CameraSerializer
from .services import verificar_camera, verificar_todas_cameras


def gerar_frames(url_stream):
    cap = cv2.VideoCapture(url_stream)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )
    cap.release()


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

    @action(detail=True, methods=['get'], authentication_classes=[], permission_classes=[AllowAny])
    def stream(self, request, pk=None):
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.exceptions import TokenError
        from apps.authentication.models import Usuario

        token = request.query_params.get('token')
        if not token:
                return Response({'erro': 'Token nao fornecido'}, status=401)

        try:
                access_token = AccessToken(token)
                usuario_id = access_token['user_id']
                Usuario.objects.get(id=usuario_id)
        except (TokenError, Usuario.DoesNotExist):
                return Response({'erro': 'Token invalido'}, status=401)

        camera = self.get_object()
        if camera.status == 'offline':
            return Response({'erro': 'Camera offline'}, status=503)

        return StreamingHttpResponse(
            gerar_frames(camera.url_stream),
            content_type='multipart/x-mixed-replace; boundary=frame'
    )