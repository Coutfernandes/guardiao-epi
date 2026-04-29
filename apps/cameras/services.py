import cv2
import threading
from .models import Camera


def verificar_camera(camera_id):
    """
    Tenta conectar ao stream RTSP da camera.
    Atualiza o status para online ou offline conforme o resultado.
    """
    try:
        camera = Camera.objects.get(id=camera_id)
        cap = cv2.VideoCapture(camera.url_stream)

        if cap.isOpened():
            camera.status = 'online'
        else:
            camera.status = 'offline'

        cap.release()
        camera.save()

    except Camera.DoesNotExist:
        pass
    except Exception:
        try:
            camera = Camera.objects.get(id=camera_id)
            camera.status = 'offline'
            camera.save()
        except Exception:
            pass


def verificar_todas_cameras():
    """
    Verifica todas as cameras ativas em threads paralelas.
    Cada camera e verificada de forma independente.
    """
    cameras = Camera.objects.filter(ativa=True)
    threads = []

    for camera in cameras:
        t = threading.Thread(target=verificar_camera, args=(camera.id,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()