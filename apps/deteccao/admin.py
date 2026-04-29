from django.contrib import admin
from .models import Ocorrencia


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('camera', 'tipo', 'status', 'pessoas_detectadas', 'criado_em')
    list_filter = ('tipo', 'status', 'camera')
    search_fields = ('camera__nome', 'camera__identificador')
    readonly_fields = ('criado_em',)