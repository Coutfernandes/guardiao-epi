from django.contrib import admin
from .models import Ocorrencia, Alerta


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('camera', 'tipo', 'status', 'pessoas_detectadas', 'criado_em')
    list_filter = ('tipo', 'status', 'camera')
    search_fields = ('camera__nome', 'camera__identificador')
    readonly_fields = ('criado_em',)


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('camera', 'nivel', 'mensagem', 'reconhecido', 'criado_em')
    list_filter = ('nivel', 'reconhecido', 'camera')
    search_fields = ('camera__nome', 'mensagem')
    readonly_fields = ('criado_em',)