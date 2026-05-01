import cv2
import os
import uuid
from datetime import datetime
from ultralytics import YOLO
from django.conf import settings


MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'yolov8n.pt')
model = None


def carregar_modelo():
    global model
    if model is None:
        pasta_models = os.path.join(settings.BASE_DIR, 'models')
        os.makedirs(pasta_models, exist_ok=True)
        caminho_modelo = os.path.join(pasta_models, 'yolov8n.pt')
        model = YOLO(caminho_modelo)
    return model


def capturar_frame(url_stream):
    cap = cv2.VideoCapture(url_stream)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    return None


def salvar_frame(frame):
    pasta = os.path.join(settings.BASE_DIR, 'media', 'frames')
    os.makedirs(pasta, exist_ok=True)
    nome = f'{uuid.uuid4()}.jpg'
    caminho = os.path.join(pasta, nome)
    cv2.imwrite(caminho, frame)
    return f'media/frames/{nome}'


def detectar_pessoas(frame):
    yolo = carregar_modelo()
    resultados = yolo(frame, classes=[0], verbose=False)
    pessoas = 0
    for r in resultados:
        pessoas += len(r.boxes)
    return pessoas


def analisar_epis_configurados(frame, epis_configurados):
    """
    Por enquanto retorna simulacao da deteccao de EPIs.
    Sera substituido pelo modelo treinado com imagens proprias.
    """
    epis_ausentes = []
    for epi in epis_configurados:
        epis_ausentes.append(epi)
    return epis_ausentes


def processar_camera(camera):
    from .models import Ocorrencia

    frame = capturar_frame(camera.url_stream)

    if frame is None:
        camera.status = 'offline'
        camera.save()
        Ocorrencia.objects.create(
            camera=camera,
            tipo='equipment_fault',
            status='nao_conforme',
            epis_ausentes=[],
            pessoas_detectadas=0,
        )
        return

    camera.status = 'online'
    camera.save()

    pessoas = detectar_pessoas(frame)

    if pessoas == 0:
        return

    frame_path = salvar_frame(frame)

    epis_configurados = list(
        camera.configuracoes_epi.filter(ativo=True).values_list('tipo_epi', flat=True)
    ) if hasattr(camera, 'configuracoes_epi') else []

    epis_ausentes = analisar_epis_configurados(frame, epis_configurados)

    if epis_ausentes:
        Ocorrencia.objects.create(
            camera=camera,
            tipo='epi_ausente',
            status='nao_conforme',
            epis_ausentes=epis_ausentes,
            frame_path=frame_path,
            pessoas_detectadas=pessoas,
        )
    else:
        Ocorrencia.objects.create(
            camera=camera,
            tipo='conformidade',
            status='conforme',
            epis_ausentes=[],
            frame_path=frame_path,
            pessoas_detectadas=pessoas,
        )