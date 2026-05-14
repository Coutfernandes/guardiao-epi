import cv2
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .models import Camera, ConfiguracaoEPI
from .serializers import CameraSerializer, ConfiguracaoEPISerializer
from .services import verificar_camera, verificar_todas_cameras


TRADUCAO_EPI = {
    'gloves': 'luvas',
    'goggles': 'oculos',
    'helmet': 'capacete',
    'no gloves': 'sem luvas',
    'no goggles': 'sem oculos',
    'no helmet': 'sem capacete',
    'no shoes': 'sem botina',
    'no vest': 'sem colete',
    'shoes': 'botina',
    'vest': 'colete'
}

CORES = {
    'no gloves': (0, 0, 255),
    'no goggles': (0, 0, 255),
    'no helmet': (0, 0, 255),
    'no shoes': (0, 0, 255),
    'no vest': (0, 0, 255),
    'gloves': (0, 255, 0),
    'goggles': (0, 255, 0),
    'helmet': (0, 255, 0),
    'shoes': (0, 255, 0),
    'vest': (0, 255, 0),
}

def gerar_frames(url_stream, camera_id=None):
    from apps.deteccao.services import carregar_modelo_epi
    
    cap = cv2.VideoCapture(url_stream)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    model_epi = carregar_modelo_epi()
    
    CLASSES_EPI = {
        0: 'gloves', 1: 'goggles', 2: 'helmet', 3: 'no gloves',
        4: 'no goggles', 5: 'no helmet', 6: 'no shoes', 7: 'no vest',
        8: 'shoes', 9: 'vest'
    }
    
    contador = 0
    ultimo_resultado = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        contador += 1

        if contador % 10 == 0:
            frame_resized = cv2.resize(frame, (320, 320))
            ultimo_resultado = model_epi(frame_resized, verbose=False)

        resultados = ultimo_resultado
        
        h_orig, w_orig = frame.shape[:2]
        escala_x = w_orig / 320
        escala_y = h_orig / 320
        
        for r in resultados:
            for box in r.boxes:
                confianca = float(box.conf[0])
                if confianca < 0.5:
                    continue
                
                classe_id = int(box.cls[0])
                classe_nome = CLASSES_EPI.get(classe_id, '')
                rotulo = TRADUCAO_EPI.get(classe_nome, classe_nome)
                cor = CORES.get(classe_nome, (255, 255, 0))
                
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                x1 = int(x1 * escala_x)
                y1 = int(y1 * escala_y)
                x2 = int(x2 * escala_x)
                y2 = int(y2 * escala_y)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
                
                texto = f'{rotulo} {confianca:.0%}'
                (tw, th), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 4, y1), cor, -1)
                cv2.putText(frame, texto, (x1 + 2, y1 - 4),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
        frame_envio = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
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

    @action(detail=True, methods=['get', 'post'])
    def epis(self, request, pk=None):
        camera = self.get_object()
        if request.method == 'GET':
            configuracoes = camera.configuracoes_epi.all()
            return Response(ConfiguracaoEPISerializer(configuracoes, many=True).data)
        elif request.method == 'POST':
            tipo_epi = request.data.get('tipo_epi')
            ativo = request.data.get('ativo', True)
            config, criado = ConfiguracaoEPI.objects.get_or_create(
                camera=camera,
                tipo_epi=tipo_epi,
                defaults={'ativo': ativo}
            )
            if not criado:
                config.ativo = ativo
                config.save()
            return Response(ConfiguracaoEPISerializer(config).data)

    @action(detail=True, methods=['get'], authentication_classes=[], permission_classes=[])
    def stream(self, request, pk=None):
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.exceptions import TokenError
        from apps.authentication.models import Usuario
        from rest_framework.permissions import AllowAny

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
            gerar_frames(camera.url_stream, camera.id),
            content_type='multipart/x-mixed-replace; boundary=frame'
)


class ConfiguracaoEPIViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoEPI.objects.all()
    serializer_class = ConfiguracaoEPISerializer

    def get_queryset(self):
        queryset = ConfiguracaoEPI.objects.all()
        camera_id = self.request.query_params.get('camera')
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        return queryset