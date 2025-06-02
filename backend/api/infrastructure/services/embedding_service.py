import requests
import os

from api.infrastructure.exceptions import EmbeddingModelError

api_url = os.environ.get("CNN_URL")

def generate_embbeding(img_bytes):
    try:
        response = requests.post(f"{api_url}/embed", data=img_bytes, headers={"Content-Type": "application/octet-stream"})
        response.raise_for_status()
        return response.json()["embedding_url"]
    except Exception as e:
        raise EmbeddingModelError("Fallo al generar embedding desde el microservicio CNN") from e
