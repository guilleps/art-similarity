import os
import random
import shutil
from pathlib import Path

ORIG_DATASET_DIR = "C:/workspace/data/train"
DEST_DATASET_DIR = "C:/workspace/data/train_sampled" 
SAMPLES_PER_CLASS = 500 # num de imágenes por clase a copiar
RANDOM_SEED = 42 # Reproducibilidad

random.seed(RANDOM_SEED)

# DIRECTORIO DESTINO
Path(DEST_DATASET_DIR).mkdir(parents=True, exist_ok=True)

# RECORRER CADA CLASE (ESTRATO)
for class_name in os.listdir(ORIG_DATASET_DIR):
    class_path = os.path.join(ORIG_DATASET_DIR, class_name)
    if not os.path.isdir(class_path):
        continue  # ignorar archivos sueltos

    dest_class_path = os.path.join(DEST_DATASET_DIR, class_name)
    Path(dest_class_path).mkdir(parents=True, exist_ok=True)

    all_images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    selected_images = random.sample(all_images, min(SAMPLES_PER_CLASS, len(all_images)))

    for img_name in selected_images:
        src_path = os.path.join(class_path, img_name)
        dst_path = os.path.join(dest_class_path, img_name)
        shutil.copy2(src_path, dst_path)

print(f"✅ Muestreo estratificado completado en '{DEST_DATASET_DIR}' con {SAMPLES_PER_CLASS} imágenes por clase.")
