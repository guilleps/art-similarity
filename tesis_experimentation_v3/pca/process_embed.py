import os
import cv2
import json
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from matplotlib import pyplot as plt
from transformers import CLIPProcessor, CLIPModel

BASE_DIR = "images/individual/3"
OUTPUT_IMG_DIR = "images/individual/3/transformed"
OUTPUT_EMB_DIR = "images/individual/3/embeddings"
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)
os.makedirs(OUTPUT_EMB_DIR, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# --- Funciones de transformación ---
def apply_contrast_enhancement(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    lab_eq = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

def apply_texture_direction(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    magnitude = cv2.magnitude(sobelx, sobely)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    return magnitude.astype(np.uint8)

def apply_color_distribution_map(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    heatmap = np.mean(img_rgb, axis=2)
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    return (plt.cm.plasma(heatmap.astype(np.uint8))[:, :, :3] * 255).astype(np.uint8)

def apply_hsv_channels(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h_vis = cv2.normalize(h, None, 0, 255, cv2.NORM_MINMAX)
    s_vis = cv2.normalize(s, None, 0, 255, cv2.NORM_MINMAX)
    v_vis = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)
    return {
        "hue": h_vis.astype(np.uint8),
        "saturation": s_vis.astype(np.uint8),
        "value": v_vis.astype(np.uint8)
    }

# extractor de embeddings
def get_clip_embedding(img_pil):
    inputs = processor(images=img_pil, return_tensors="pt").to(device)
    with torch.no_grad():
        features = model.get_image_features(**inputs)
    return features[0].cpu().numpy()


for filename in tqdm(os.listdir(BASE_DIR), desc="Procesando imágenes"):
    if not filename.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    name_wo_ext = os.path.splitext(filename)[0]
    image_path = os.path.join(BASE_DIR, filename)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (256, 256))

    transforms = {
        "contrast": apply_contrast_enhancement(image),
        "texture": apply_texture_direction(image),
        "color_map": apply_color_distribution_map(image),
        **apply_hsv_channels(image)
    }

    for tname, timg in transforms.items():
        save_img_path = os.path.join(OUTPUT_IMG_DIR, f"{name_wo_ext}_{tname}.jpg")
        emb_path = os.path.join(OUTPUT_EMB_DIR, f"{name_wo_ext}_{tname}_embedding.json")

        # Guardar imagen transformada
        if len(timg.shape) == 2:  # escala de grises
            cv2.imwrite(save_img_path, timg)
            img_pil = Image.fromarray(cv2.cvtColor(cv2.imread(save_img_path), cv2.COLOR_BGR2RGB))
        else:
            cv2.imwrite(save_img_path, cv2.cvtColor(timg, cv2.COLOR_RGB2BGR))
            img_pil = Image.fromarray(timg)

        # Obtener y guardar embedding
        emb = get_clip_embedding(img_pil)
        with open(emb_path, "w") as f:
            json.dump(emb.tolist(), f)

print("✅ Proceso completo. Imágenes transformadas y embeddings guardados.")

