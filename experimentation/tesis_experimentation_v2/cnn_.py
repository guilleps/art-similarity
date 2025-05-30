import os
import cv2
import json
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel
from matplotlib import pyplot as plt
from utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels
)

INPUT_DIR = "images/5"
TRANSFORMED_DIR = "images/5/transformed_images"
EMBEDDINGS_DIR = "images/5/embeddings"

def save_transformed_images(image_path, output_base_dir):
    image = cv2.imread(image_path)
    name = os.path.splitext(os.path.basename(image_path))[0]
    output_dir = os.path.join(output_base_dir, name)
    os.makedirs(output_dir, exist_ok=True)

    # Contraste
    contrast = apply_contrast_enhancement(image)
    cv2.imwrite(os.path.join(output_dir, f"{name}_contrast.jpg"), contrast)

    # Textura
    texture = apply_texture_direction(image)
    cv2.imwrite(os.path.join(output_dir, f"{name}_texture.jpg"), texture)

    # Mapa de calor
    color_map = apply_color_distribution_map(image)
    plt.imsave(os.path.join(output_dir, f"{name}_color_map.jpg"), color_map)

    # HSV
    hsv_channels = apply_hsv_channels(image)
    for channel, img in hsv_channels.items():
        cv2.imwrite(os.path.join(output_dir, f"{name}_hsv_{channel}.jpg"), img)

    return output_dir

def extract_clip_embeddings(image_path, model, processor, device):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    return outputs[0].cpu().numpy().tolist()

def process_transformed_folder(transformed_dir, embeddings_output_dir, model, processor, device):
    os.makedirs(embeddings_output_dir, exist_ok=True)
    for img_name in os.listdir(transformed_dir):
        if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        img_path = os.path.join(transformed_dir, img_name)
        embedding = extract_clip_embeddings(img_path, model, processor, device)

        name_wo_ext = os.path.splitext(img_name)[0]
        with open(os.path.join(embeddings_output_dir, f"{name_wo_ext}_embedding.json"), "w") as f:
            json.dump(embedding, f)

def run_pipeline():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    image_paths = [
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    for image_path in tqdm(image_paths, desc="Procesando imágenes"):
        name = os.path.splitext(os.path.basename(image_path))[0]

        # Paso 1: Transformar
        transformed_subfolder = save_transformed_images(image_path, TRANSFORMED_DIR)

        # Paso 2: Extraer embeddings
        embedding_subfolder = os.path.join(EMBEDDINGS_DIR, name)
        process_transformed_folder(transformed_subfolder, embedding_subfolder, model, processor, device)


if __name__ == "__main__":
    run_pipeline()
