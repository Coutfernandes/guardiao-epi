import cv2
import os
import uuid
from ultralytics import YOLO
from django.conf import settings

model_pessoas = None
model_epi = None

CLASSES_EPI = {
    0: 'gloves',
    1: 'goggles',
    2: 'helmet',
    3: 'no gloves',
    4: 'no goggles',
    5: 'no helmet',
    6: 'no shoes',
    7: 'no vest',
    8: 'shoes',
    9: 'vest'
}

EPIS_AUSENTES = ['no gloves', 'no goggles', 'no helmet', 'no shoes', 'no vest']
EPIS_PRESENTES = ['gloves', 'goggles', 'helmet', 'shoes', 'vest']


def carregar_modelo():
    global model_pessoas
    if model_pessoas is None:
        pasta_models = os.path.join(settings.BASE_DIR, 'models')
        os.makedirs(pasta_models, exist_ok=True)
        caminho_modelo = os.path.join(pasta_models, 'yolov8n.pt')
        model_pessoas = YOLO(caminho_modelo)
    return model_pessoas


def carregar_modelo_epi():
    global model_epi
    if model_epi is None:
        caminho = os.path.join(settings.BASE_DIR, 'models', 'epi_detector.pt')
        model_epi = YOLO(caminho)
    return model_epi


def capturar_frame(url_stream):
    cap = cv2.VideoCapture(url_stream)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    return None


def preprocessar_frame(frame, largura=640, altura=640):
    frame_redimensionado = cv2.resize(frame, (largura, altura))
    return frame_redimensionado


def salvar_frame(frame):
    pasta = os.path.join(settings.BASE_DIR, 'media', 'frames')
    os.makedirs(pasta, exist_ok=True)
    nome = f'{uuid.uuid4()}.jpg'
    caminho = os.path.join(pasta, nome)
    cv2.imwrite(caminho, frame)
    return f'media/frames/{nome}'


def detectar_pessoas(frame):
    yolo = carregar_modelo()
    frame_processado = preprocessar_frame(frame)
    resultados = yolo(frame_processado, classes=[0], verbose=False)
    pessoas = 0
    for r in resultados:
        pessoas += len(r.boxes)
    return pessoas


def detectar_epis(frame):
    yolo = carregar_modelo_epi()
    frame_processado = preprocessar_frame(frame)
    resultados = yolo(frame_processado, verbose=False)
    epis_ausentes = []
    epis_presentes = []
    for r in resultados:
        for box in r.boxes:
            classe_id = int(box.cls[0])
            classe_nome = CLASSES_EPI.get(classe_id, '')
            confianca = float(box.conf[0])
            if confianca > 0.5:
                if classe_nome in EPIS_AUSENTES:
                    epis_ausentes.append(classe_nome)
                elif classe_nome in EPIS_PRESENTES:
                    epis_presentes.append(classe_nome)
    return epis_ausentes, epis_presentes

def gerar_alerta(camera, ocorrencia):
    """
    Gera alerta respeitando cooldown de 2 minutos por camera.
    Regra RN16: aguardar 2 minutos antes de novo alerta para a mesma camera.
    """
    from .models import Alerta
    from django.utils import timezone
    from datetime import timedelta

    dois_minutos_atras = timezone.now() - timedelta(minutes=2)
    alerta_recente = Alerta.objects.filter(
        camera=camera,
        criado_em__gte=dois_minutos_atras
    ).exists()

    if alerta_recente:
        return None

    if ocorrencia.tipo == 'epi_ausente':
        nivel = 'critico'
        epis = ', '.join(ocorrencia.epis_ausentes)
        mensagem = f'EPIs ausentes detectados na camera {camera.identificador}: {epis}'
    elif ocorrencia.tipo == 'equipment_fault':
        nivel = 'aviso'
        mensagem = f'Camera {camera.identificador} perdeu conexao'
    else:
        return None

    alerta = Alerta.objects.create(
        ocorrencia=ocorrencia,
        camera=camera,
        nivel=nivel,
        mensagem=mensagem,
    )
    return alerta

def processar_camera(camera):
    from .models import Ocorrencia

    frame = capturar_frame(camera.url_stream)

    if frame is None:
        camera.status = 'offline'
        camera.save()
        ocorrencia = Ocorrencia.objects.create(
            camera=camera,
            tipo='equipment_fault',
            status='nao_conforme',
            epis_ausentes=[],
            pessoas_detectadas=0,
        )
        gerar_alerta(camera, ocorrencia)
        return

    camera.status = 'online'
    camera.save()

    pessoas = detectar_pessoas(frame)

    if pessoas == 0:
        return

    frame_path = salvar_frame(frame)
    epis_ausentes, epis_presentes = detectar_epis(frame)

    if epis_ausentes:
        ocorrencia = Ocorrencia.objects.create(
            camera=camera,
            tipo='epi_ausente',
            status='nao_conforme',
            epis_ausentes=epis_ausentes,
            frame_path=frame_path,
            pessoas_detectadas=pessoas,
        )
        gerar_alerta(camera, ocorrencia)
    else:
        Ocorrencia.objects.create(
            camera=camera,
            tipo='conformidade',
            status='conforme',
            epis_ausentes=[],
            frame_path=frame_path,
            pessoas_detectadas=pessoas,
        )