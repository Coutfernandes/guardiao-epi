from rest_framework import serializers
from .models import Camera, ConfiguracaoEPI


class ConfiguracaoEPISerializer(serializers.ModelSerializer):
    tipo_epi_display = serializers.CharField(source='get_tipo_epi_display', read_only=True)

    class Meta:
        model = ConfiguracaoEPI
        fields = '__all__'
        read_only_fields = ['criado_em']


class CameraSerializer(serializers.ModelSerializer):
    configuracoes_epi = ConfiguracaoEPISerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em']