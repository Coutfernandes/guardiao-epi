from django.db import models


class Camera(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('alerta', 'Alerta'),
    ]

    nome = models.CharField(max_length=100)
    identificador = models.CharField(max_length=20, unique=True)
    url_stream = models.CharField(max_length=255)
    setor = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.identificador} - {self.nome}'

    class Meta:
        ordering = ['identificador']

class ConfiguracaoEPI(models.Model):
    TIPOS_EPI = [
        ('helmet','Capacete'),
        ('gloves','Luvas'),
        ('goggles','Oculos de Protecao'),
        ('vest','Colete Refletivo'),
        ('shoes','Botina de Seguranca'),
        ('mask','Mascara'),
    ]
    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        related_name='configuracoes_epi'
    )
    tipo_epi = models.CharField(max_length=20, choices=TIPOS_EPI)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.camera.identificador} - {self.tipo_epi}'

    class Meta:
        unique_together = ['camera', 'tipo_epi']
        ordering = ['camera', 'tipo_epi']