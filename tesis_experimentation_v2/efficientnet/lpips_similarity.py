import os
import json
import lpips
import torch
import torchvision.transforms as transforms
from PIL import Image
import logging
from logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

lpips_model = lpips.LPIPS(net='alex')  # También puedes usar 'vgg'

def get_transform_key(filename):
    parts = filename.split(".")[0].split("_")
    if "hsv" in filename:
        return f"hsv_{parts[-1]}"
    elif "color_map" in filename:
        return "heat_color_map"
    elif "contrast" in filename:
        return "contrast"
    elif "texture" in filename:
        return "texture"
    else:
        return "unknown"

def compare_lpips_images(image1_folder, image2_folder, output_json_path):
    transform = transforms.ToTensor()

    results = {}

    image1_files = {get_transform_key(f): f for f in os.listdir(image1_folder) if f.endswith((".jpg", ".png"))}
    image2_files = {get_transform_key(f): f for f in os.listdir(image2_folder) if f.endswith((".jpg", ".png"))}

    for key in image1_files:
        if key in image2_files:
            img1_path = os.path.join(image1_folder, image1_files[key])
            img2_path = os.path.join(image2_folder, image2_files[key])

            img1 = transform(Image.open(img1_path).convert('RGB')).unsqueeze(0)
            img2 = transform(Image.open(img2_path).convert('RGB')).unsqueeze(0)

            with torch.no_grad():
                dist = lpips_model(img1, img2).item()

            similarity = 1 - dist  # LPIPS es una distancia, la invertimos
            similarity = round(max(0, min(1, similarity)), 4)

            results[key] = {
                "files": [image1_files[key], image2_files[key]],
                "similarity": similarity
            }

            logger.info(f"LPIPS similitud para '{key}': {similarity:.4f}")

    with open(output_json_path, "w") as f:
        json.dump(results, f, indent=4)

    logger.info(f"Guardado resultados LPIPS en: {output_json_path}")
