from rest_framework import serializers
from .models import Ocorrencia


class OcorrenciaSerializer(serializers.ModelSerializer):
    camera_nome = serializers.CharField(source='camera.nome', read_only=True)
    camera_identificador = serializers.CharField(source='camera.identificador', read_only=True)

    class Meta:
        model = Ocorrencia
        fields = '__all__'
        read_only_fields = ['criado_em']