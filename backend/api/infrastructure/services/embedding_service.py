import requests
import os

from api.infrastructure.exceptions import EmbeddingModelError

def generate_embbeding(img_bytes):
    try:
        response = requests.post(f"http://localhost:8002/embed", data=img_bytes, headers={"Content-Type": "image/jpeg"})
        response.raise_for_status()
        return response.json()["embedding_url"]
    except Exception as e:
        raise EmbeddingModelError("Fallo al generar embedding desde el microservicio CNN") from e
