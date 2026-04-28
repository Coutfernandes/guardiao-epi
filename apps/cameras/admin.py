from django.contrib import admin
from .models import Camera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'nome', 'setor', 'status', 'ativa')
    list_filter = ('status', 'ativa', 'setor')
    search_fields = ('nome', 'identificador', 'setor')