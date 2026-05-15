from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, LogAuditoria


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'perfil', 'is_active')
    list_filter = ('perfil', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil', {'fields': ('perfil',)}),
    )


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao', 'descricao', 'ip', 'criado_em')
    list_filter = ('acao', 'usuario')
    search_fields = ('usuario__username', 'descricao')
    readonly_fields = ('usuario', 'acao', 'descricao', 'ip', 'criado_em')