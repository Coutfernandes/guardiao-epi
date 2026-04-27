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