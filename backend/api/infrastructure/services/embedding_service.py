import numpy as np
import requests
from PIL import Image
import io

from api.infrastructure.exceptions import EmbeddingModelError

def generate_embbeding(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).resize((224, 224)).convert("RGB")
    img_array = np.array(img).astype("float32")

    payload = { "instances": [img_array.tolist()] }

    try:
        print("📤 Enviando imagen a TensorFlow Serving...")
        response = requests.post("http://localhost:8501/v1/models/efficientnet:predict", json=payload)
        response.raise_for_status()
        embedding = response.json()['predictions'][0]
        print("✅ Embedding generado (primeros 5 valores):", embedding[:5])
        return embedding
    except Exception as e:
        print("❌ Error al generar embedding:", e)
        raise EmbeddingModelError() from e