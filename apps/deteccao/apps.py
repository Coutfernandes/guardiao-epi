from django.apps import AppConfig


class DeteccaoConfig(AppConfig):
    name = 'apps.deteccao'

    def ready(self):
        from .scheduler import iniciar_scheduler
        iniciar_scheduler()