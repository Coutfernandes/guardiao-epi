from django.db import models
from apps.cameras.models import Camera


class Ocorrencia(models.Model):
    STATUS_CHOICES = [
        ('conforme', 'Conforme'),
        ('nao_conforme', 'Nao Conforme'),
    ]

    TIPO_CHOICES = [
        ('epi_ausente', 'EPI Ausente'),
        ('equipment_fault', 'Falha de Equipamento'),
        ('conformidade', 'Conformidade'),
    ]

    camera = models.ForeignKey(Camera, on_delete=models.PROTECT, related_name='ocorrencias')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='nao_conforme')
    epis_ausentes = models.JSONField(default=list)
    frame_path = models.CharField(max_length=255, blank=True)
    pessoas_detectadas = models.IntegerField(default=0)
    confianca = models.FloatField(default=0.0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.camera.identificador} - {self.tipo} - {self.criado_em}'

    class Meta:
        ordering = ['-criado_em']

class Alerta(models.Model):
    NIVEL_CHOICES = [
        ('critico', 'Critico'),
        ('aviso', 'Aviso'),
        ('info', 'Info'),
    ]

    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name='alertas')
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='alertas')
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='aviso')
    mensagem = models.TextField()
    reconhecido = models.BooleanField(default=False)
    reconhecido_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.camera.identificador} - {self.nivel} - {self.criado_em}'

    class Meta:
        ordering = ['-criado_em']