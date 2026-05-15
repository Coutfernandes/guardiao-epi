from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    PERFIL_CHOICES = [
        ('administrador', 'Administrador'),
        ('supervisor', 'Supervisor'),
    ]

    perfil = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        default='supervisor',
    )

    def __str__(self):
        return f'{self.username} ({self.perfil})'
    
class LogAuditoria(models.Model):
    ACOES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('criar_camera', 'Criar Camera'),
        ('editar_camera', 'Editar Camera'),
        ('deletar_camera', 'Deletar Camera'),
        ('reconhecer_alerta', 'Reconhecer Alerta'),
        ('gerar_relatorio', 'Gerar Relatorio'),
        ('configurar_epi', 'Configurar EPI'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs'
    )
    acao = models.CharField(max_length=30, choices=ACOES)
    descricao = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario} - {self.acao} - {self.criado_em}'

    class Meta:
        ordering = ['-criado_em']