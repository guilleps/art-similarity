import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel

# Cargar modelo y procesador
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)

# Cargar imagen
image = Image.open("gato.jpeg")

# Lista de textos candidatos
texts = ["a dog", "a cat", "a bird"]

# Preprocesar inputs
inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

# Obtener similitudes
with torch.no_grad():
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # [1, N textos]
    probs = logits_per_image.softmax(dim=1)      # Probabilidades

# Mostrar resultados
for label, prob in zip(texts, probs[0]):
    print(f"{label}: {prob:.4f}")
