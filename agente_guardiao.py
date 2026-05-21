import cv2
import requests
import base64
import time
import argparse
import threading
from ultralytics import YOLO
from http.server import BaseHTTPRequestHandler, HTTPServer

# ============================================================
# CONFIGURACOES
# ============================================================
DJANGO_URL = 'http://127.0.0.1:8000/api/deteccao/receber/'
CAMERA_ID = 1
STREAM_PORT = 8080
INTERVALO_DETECCAO = 10  # Processar IA a cada N frames
CONFIANCA_MINIMA = 0.5

CLASSES_EPI = {
    0: 'gloves', 1: 'goggles', 2: 'helmet', 3: 'no gloves',
    4: 'no goggles', 5: 'no helmet', 6: 'no shoes', 7: 'no vest',
    8: 'shoes', 9: 'vest'
}

EPIS_AUSENTES = ['no gloves', 'no goggles', 'no helmet', 'no shoes', 'no vest']
EPIS_PRESENTES = ['gloves', 'goggles', 'helmet', 'shoes', 'vest']

TRADUCAO = {
    'no helmet': 'sem capacete', 'no gloves': 'sem luvas',
    'no goggles': 'sem oculos', 'no vest': 'sem colete', 'no shoes': 'sem botina',
    'helmet': 'capacete', 'gloves': 'luvas', 'goggles': 'oculos',
    'vest': 'colete', 'shoes': 'botina'
}

CORES = {
    'no gloves': (0, 0, 255), 'no goggles': (0, 0, 255),
    'no helmet': (0, 0, 255), 'no shoes': (0, 0, 255), 'no vest': (0, 0, 255),
    'gloves': (0, 255, 0), 'goggles': (0, 255, 0), 'helmet': (0, 255, 0),
    'shoes': (0, 255, 0), 'vest': (0, 255, 0),
}

# ============================================================
# ESTADO GLOBAL DO AGENTE (THREAD-SAFE)
# ============================================================
frame_bruto = None      # Armazena o frame capturado direto da câmera
frame_mjpeg = None      # Armazena o frame final (com ou sem desenhos) pronto para stream
frame_lock = threading.Lock()
executando = True

# ============================================================
# CARREGAR MODELOS
# ============================================================
def carregar_modelos():
    print('[AGENTE] Carregando modelos YOLOv8...')
    modelo_pessoas = YOLO('models/yolov8n.pt')
    modelo_epi = YOLO('models/epi_detector.pt')
    print('[AGENTE] Modelos carregados.')
    return modelo_pessoas, modelo_epi

# ============================================================
# THREAD EXCLUSIVA DE CAPTURA (ANTI-DELAY / LIMPA BUFFER)
# ============================================================
def thread_captura_camera(url_rtsp):
    global frame_bruto, executando
    cap = cv2.VideoCapture(url_rtsp)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # Mantém o buffer no mínimo

    if not cap.isOpened():
        print('[AGENTE] Erro crítico: Câmera offline.')
        disparar_alerta_django('equipment_fault', 'nao_conforme', 0, [], None, 'offline')
        executando = False
        return

    while executando:
        ret, frame = cap.read()
        if not ret:
            print('[AGENTE] Falha de leitura. Tentando reconectar...')
            time.sleep(2)
            cap = cv2.VideoCapture(url_rtsp)
            continue
        
        with frame_lock:
            frame_bruto = frame.copy()
            
    cap.release()

# ============================================================
# ENVIAR DADOS PARA O DJANGO (ASSÍNCRONO)
# ============================================================
def disparar_alerta_django(tipo, status_ocorrencia, pessoas, epis_ausentes, frame, status_camera):
    # Roda em uma thread separada para não travar o processamento visual
    def worker():
        try:
            frame_b64 = ''
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                frame_b64 = base64.b64encode(buffer).decode('utf-8')

            payload = {
                'camera_id': CAMERA_ID,
                'tipo': tipo,
                'status_ocorrencia': status_ocorrencia,
                'pessoas_detectadas': pessoas,
                'epis_ausentes': epis_ausentes,
                'frame_b64': frame_b64,
                'status_camera': status_camera,
            }
            res = requests.post(DJANGO_URL, json=payload, timeout=5)
            print(f'[AGENTE] API Django notificada: {tipo} | Status: {res.status_code}')
        except Exception as e:
            print(f'[AGENTE] Erro na requisição de alerta: {e}')

    threading.Thread(target=worker, daemon=True).start()

# ============================================================
# SERVIDOR MJPEG FLUIDO (PORTA 8080)
# ============================================================
class MJPEGHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass 

    def do_GET(self):
        if self.path == '/stream':
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            try:
                while executando:
                    with frame_lock:
                        if frame_mjpeg is None:
                            time.sleep(0.01)
                            continue
                        _, buffer = cv2.imencode('.jpg', frame_mjpeg, [cv2.IMWRITE_JPEG_QUALITY, 75])
                        frame_bytes = buffer.tobytes()

                    self.wfile.write(b'--frame\r\n')
                    self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n')
                    self.wfile.write(frame_bytes)
                    self.wfile.write(b'\r\n')
                    time.sleep(0.033)  # Limita a entrega a ~30 FPS na web de forma suave
            except Exception:
                pass
        else:
            self.send_response(404)
            self.end_headers()

def iniciar_servidor_mjpeg():
    servidor = HTTPServer(('0.0.0.0', STREAM_PORT), MJPEGHandler)
    print(f'[AGENTE] Stream fluido disponível em http://localhost:{STREAM_PORT}/stream')
    servidor.serve_forever()

# ============================================================
# LOOP PRINCIPAL DE PROCESSAMENTO DA IA
# ============================================================
def loop_processamento_ia(modelo_pessoas, modelo_epi):
    global frame_mjpeg
    contador = 0
    caixas_acumuladas = [] # Guarda os desenhos das detecções passadas para manter o FPS visual alto

    print('[AGENTE] Loop de Inteligência Artificial iniciado.')
    
    while executando:
        with frame_lock:
            if frame_bruto is None:
                time.sleep(0.01)
                continue
            frame_trabalho = frame_bruto.copy()

        contador += 1

        # A IA executa de forma espaçada, mas o vídeo continua renderizando frame a frame
        if contador % INTERVALO_DETECCAO == 0:
            frame_resized = cv2.resize(frame_trabalho, (320, 320))

            # Detectar pessoas
            res_pessoas = modelo_pessoas(frame_resized, classes=[0], verbose=False)
            pessoas = sum(len(r.boxes) for r in res_pessoas)

            epis_ausentes = []
            caixas_acumuladas = []

            if pessoas > 0:
                res_epi = modelo_epi(frame_resized, verbose=False)
                h, w = frame_trabalho.shape[:2]
                ex, ey = w / 320, h / 320

                for r in res_epi:
                    for box in r.boxes:
                        conf = float(box.conf[0])
                        if conf < CONFIANCA_MINIMA:
                            continue
                        cls = CLASSES_EPI.get(int(box.cls[0]), '')
                        rotulo = TRADUCAO.get(cls, cls)
                        cor = CORES.get(cls, (255, 255, 0))

                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        x1, y1, x2, y2 = int(x1*ex), int(y1*ey), int(x2*ex), int(y2*ey)
                        
                        # Guarda a detecção atualizada para pintar nos próximos frames
                        caixas_acumuladas.append((x1, y1, x2, y2, cor, f'{rotulo} {conf:.0%}'))

                        if cls in EPIS_AUSENTES:
                            epis_ausentes.append(cls)

                # Dispara os alertas para o Django de forma assíncrona (não trava o loop)
                if epis_ausentes:
                    disparar_alerta_django('epi_ausente', 'nao_conforme', pessoas, epis_ausentes, frame_trabalho, 'online')
                else:
                    disparar_alerta_django('conformidade', 'conforme', pessoas, [], frame_trabalho, 'online')

        # Aplica as caixas de marcação em tempo real no frame atual
        for x1, y1, x2, y2, cor, texto in caixas_acumuladas:
            cv2.rectangle(frame_trabalho, (x1, y1), (x2, y2), cor, 2)
            (tw, th), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame_trabalho, (x1, y1-th-6), (x1+tw+4, y1), cor, -1)
            cv2.putText(frame_trabalho, texto, (x1+2, y1-4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Atualiza o frame de transmissão de forma contínua e redimensionada
        frame_renderizado = cv2.resize(frame_trabalho, (640, 480))
        with frame_lock:
            frame_mjpeg = frame_renderizado
            
        # Pequena folga para aliviar o processador da máquina local
        time.sleep(0.01)

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Agente Guardiao EPI')
    parser.add_argument('--rtsp', type=str,
                        default='rtsp://admin:Tcc2026daniel@192.168.0.14:554/cam/realmonitor?channel=1&subtype=1',
                        help='URL RTSP da camera')
    parser.add_argument('--django', type=str,
                        default='http://127.0.0.1:8000/api/deteccao/receber/',
                        help='URL do endpoint Django')
    parser.add_argument('--camera-id', type=int, default=1,
                        help='ID da camera no banco de dados Django')
    parser.add_argument('--porta', type=int, default=8080,
                        help='Porta do stream MJPEG local')
    args = parser.parse_args()

    DJANGO_URL = args.django
    CAMERA_ID = args.camera_id
    STREAM_PORT = args.porta

    modelo_pessoas, modelo_epi = carregar_modelos()

    # 1. Inicia o servidor HTTP de streaming
    thread_stream = threading.Thread(target=iniciar_servidor_mjpeg, daemon=True)
    thread_stream.start()

    # 2. Inicia a captura assíncrona da câmera (Garante latência zero / impede buffer atrasado)
    thread_captura = threading.Thread(target=thread_captura_camera, args=(args.rtsp,), daemon=True)
    thread_captura.start()

    # 3. Executa o loop de IA e renderização na thread principal
    loop_processamento_ia(modelo_pessoas, modelo_epi)