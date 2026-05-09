from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Ocorrencia, Alerta
from .serializers import OcorrenciaSerializer, AlertaSerializer
from .services import processar_camera
from apps.cameras.models import Camera


class OcorrenciaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

    def get_queryset(self):
        queryset = Ocorrencia.objects.all()
        camera_id = self.request.query_params.get('camera')
        tipo = self.request.query_params.get('tipo')
        status = self.request.query_params.get('status')
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=False, methods=['post'])
    def processar(self, request):
        camera_id = request.data.get('camera_id')
        try:
            camera = Camera.objects.get(id=camera_id, ativa=True)
            processar_camera(camera)
            return Response({'mensagem': 'Camera processada com sucesso'})
        except Camera.DoesNotExist:
            return Response({'erro': 'Camera nao encontrada'}, status=404)


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

    def get_queryset(self):
        queryset = Alerta.objects.all()
        camera_id = self.request.query_params.get('camera')
        nivel = self.request.query_params.get('nivel')
        reconhecido = self.request.query_params.get('reconhecido')
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        if nivel:
            queryset = queryset.filter(nivel=nivel)
        if reconhecido is not None:
            queryset = queryset.filter(reconhecido=reconhecido == 'true')
        return queryset

    @action(detail=True, methods=['patch'])
    def reconhecer(self, request, pk=None):
        alerta = self.get_object()
        alerta.reconhecido = True
        alerta.reconhecido_em = timezone.now()
        alerta.save()
        return Response(AlertaSerializer(alerta).data)

    @action(detail=False, methods=['get'])
    def nao_reconhecidos(self, request):
        alertas = Alerta.objects.filter(reconhecido=False)
        return Response(AlertaSerializer(alertas, many=True).data)