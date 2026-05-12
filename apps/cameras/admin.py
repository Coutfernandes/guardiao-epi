from django.contrib import admin
from .models import Camera, ConfiguracaoEPI


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'nome', 'setor', 'status', 'ativa')
    list_filter = ('status', 'ativa', 'setor')
    search_fields = ('nome', 'identificador', 'setor')


@admin.register(ConfiguracaoEPI)
class ConfiguracaoEPIAdmin(admin.ModelAdmin):
    list_display = ('camera', 'tipo_epi', 'ativo', 'criado_em')
    list_filter = ('tipo_epi', 'ativo', 'camera')
    search_fields = ('camera__nome', 'camera__identificador')