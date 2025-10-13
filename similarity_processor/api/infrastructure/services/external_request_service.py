import requests
from requests.exceptions import RequestException
import logging
import time

logger = logging.getLogger(__name__)

class ExternalRequestService:
    def __init__(self, retries=3, timeout=10):
        self.retries = retries
        self.timeout = timeout

    @staticmethod
    def fetch_json(url: str) -> dict:
        for attempt in range(1, 3 + 1):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                logger.warning(f"[Intento {attempt}] Falló la solicitud a {url}: {e}")
                time.sleep(1)  # pequeño delay entre reintentos
        logger.error(f"No se pudo obtener JSON de {url} tras {3} intentos")
        raise Exception(f"Error al obtener JSON desde {url}")
    

    def fetch_bytes(self, url: str) -> bytes:
        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.content
            except requests.RequestException as e:
                logger.warning(f"[Intento {attempt}] Falló descarga binaria desde {url}: {e}")
                time.sleep(1)
        raise Exception(f"Error al obtener bytes desde {url}")
    
    
    def post_image_and_get_json(self, url, img_bytes, headers=None):
        for attempt in range(1, self.retries + 1):
            try:
                response = requests.post(url, data=img_bytes, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                logger.warning(f"[Intento {attempt}] Falló POST a {url}: {e}")
                time.sleep(1)
        logger.error(f"No se pudo POSTear imagen a {url}")
        raise Exception(f"Error al postear imagen en {url}")
