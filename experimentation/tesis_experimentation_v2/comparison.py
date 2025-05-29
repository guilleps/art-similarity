import os
import cv2
import torch
import lpips
import numpy as np
import pandas as pd
from tqdm import tqdm
from pytorch_msssim import ms_ssim
from torchvision import transforms
import random

# Inicializar LPIPS
lpips_model = lpips.LPIPS(net='alex')
lpips_model.eval()

# Transformación para LPIPS y MS-SSIM
to_tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224))
])

def load_image_tensor(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tensor = to_tensor(img).unsqueeze(0) * 2 - 1
    return tensor

def calculate_lpips(img1_tensor, img2_tensor): # Percepción visual global y semántica
    with torch.no_grad():
        return 1 - lpips_model(img1_tensor, img2_tensor).item()  # invertido para que mayor = más similar

def calculate_msssim(img1_tensor, img2_tensor): # Estructura, luminancia y contraste
    with torch.no_grad():
        return ms_ssim(img1_tensor, img2_tensor, data_range=2.0).item()

def main(folder_path, output_csv='resultados_similitud_1000.csv'):
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))] # RECORRE TODO

    if len(image_paths) < 2:
        print("⚠️ Se requieren al menos 2 imágenes.")
        return

    results = []

    print("🔍 Procesando imágenes...")

    # --------------------------------------- RECORRE SOLO LOS INDICADOS
    # nombres_base = [
    #     "antoine-blanchard_boulevard-de-la-madeleine-2.jpg",
    # ]
    # sample_images = [img for img in image_paths if os.path.basename(img) in nombres_base]


    # sample_size = 25
    # sample_images = random.sample(image_paths, sample_size)

    # if not sample_images:
    #     print("⚠️ No se encontraron coincidencias con los nombres proporcionados.")
    #     return

    # for base_path in tqdm(sample_images):
    # ---------------------------------------

    for base_path in tqdm(image_paths):
        base_tensor = load_image_tensor(base_path)

        best_lpips_sim = -1
        best_msssim_sim = -1
        best_lpips_path = ""
        best_msssim_path = ""

        for other_path in image_paths:
            if base_path == other_path:
                continue

            other_tensor = load_image_tensor(other_path)

            try:
                lpips_sim = calculate_lpips(base_tensor, other_tensor)
                msssim_sim = calculate_msssim(base_tensor, other_tensor)
            except Exception as e:
                print(f"Error comparando {base_path} con {other_path}: {e}")
                continue

            if lpips_sim > best_lpips_sim:
                best_lpips_sim = lpips_sim
                best_lpips_path = other_path

            if msssim_sim > best_msssim_sim:
                best_msssim_sim = msssim_sim
                best_msssim_path = other_path

        results.append({
            "imagen_base": base_path,
            "par_lpips": best_lpips_path,
            "lpips_sim": round(best_lpips_sim, 4),
            "par_msssim": best_msssim_path,
            "ms_ssim": round(best_msssim_sim, 4)
        })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Resultados guardados en: {output_csv}")

if __name__ == "__main__":
    folder = input("📂 Ingresa la ruta de la carpeta de imágenes: ").strip()
    main(folder)
