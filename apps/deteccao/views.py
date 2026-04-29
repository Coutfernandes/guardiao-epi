from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ocorrencia
from .serializers import OcorrenciaSerializer
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