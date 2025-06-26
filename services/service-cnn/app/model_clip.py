import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
import logging

logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def generate_embedding(image_path: str):
    try:
        logger.info("Procesando imagen para generar embedding...")
        image = Image.open(image_path)
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)
        logger.info("Embedding generado con éxito.")
        return outputs[0].cpu().numpy().tolist()
    except Exception as e:
        logger.exception("Error al generar el embedding:")
        raise
        