from django.apps import AppConfig


class DeteccaoConfig(AppConfig):
    name = 'apps.deteccao'

    def ready(self):
        pass  # Scheduler desativado - processamento feito pelo agente local