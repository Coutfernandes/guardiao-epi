import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

logger = logging.getLogger(__name__)
scheduler = None


def processar_cameras_agendado():
    """
    Funcao executada automaticamente a cada 1 minuto.
    Processa todas as cameras ativas do sistema.
    """
    try:
        from apps.cameras.models import Camera
        from apps.deteccao.services import processar_camera

        cameras = Camera.objects.filter(ativa=True)
        logger.info(f'Processando {cameras.count()} cameras')

        for camera in cameras:
            try:
                processar_camera(camera)
                logger.info(f'Camera {camera.identificador} processada')
            except Exception as e:
                logger.error(f'Erro ao processar camera {camera.identificador}: {e}')

    except Exception as e:
        logger.error(f'Erro no agendador: {e}')


def iniciar_scheduler():
    global scheduler
    if scheduler is not None:
        return

    scheduler = BackgroundScheduler(timezone='America/Manaus')
    scheduler.add_job(
        processar_cameras_agendado,
        trigger=IntervalTrigger(minutes=1),
        id='processar_cameras',
        replace_existing=True
    )
    scheduler.start()
    logger.info('Scheduler iniciado - processando cameras a cada 1 minuto')


def parar_scheduler():
    global scheduler
    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None
        logger.info('Scheduler parado')