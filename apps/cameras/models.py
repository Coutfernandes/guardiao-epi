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