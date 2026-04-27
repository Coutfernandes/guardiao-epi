from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'perfil', 'is_active', 'is_staff')
    list_filter = ('perfil', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil do Sistema', {'fields': ('perfil',)}),
    )