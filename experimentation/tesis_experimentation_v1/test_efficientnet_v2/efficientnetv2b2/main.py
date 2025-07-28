import json
from pathlib import Path
import sys

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import (
    EfficientNetB2,
    preprocess_input,
)

# Configuración del modelo (EfficientNetB2 con 260x260)
MODEL = EfficientNetB2(include_top=False, weights="imagenet", pooling="avg")
EMB_DIM = MODEL.output_shape[-1]  # 1280

# Extensiones de imagen aceptadas
IMAGE_EXTS = {".jpg", ".jpeg"}

def load_and_preprocess(img_path: Path) -> np.ndarray:
    img = image.load_img(img_path, target_size=(260, 260))
    x = image.img_to_array(img)
    x = np.expand_dims(x, 0)
    return preprocess_input(x)

def get_embedding(tensor: np.ndarray) -> np.ndarray:
    return MODEL(tensor).numpy().squeeze()

def save_results(img_path: Path, emb: np.ndarray, store_dir: Path) -> None:
    imgs_dir = store_dir / "images"
    emb_dir = store_dir / "embeddings"
    imgs_dir.mkdir(parents=True, exist_ok=True)
    emb_dir.mkdir(parents=True, exist_ok=True)

    # Copiar imagen
    target_img = imgs_dir / img_path.name
    if img_path.resolve() != target_img.resolve():
        target_img.write_bytes(img_path.read_bytes())

    # Guardar embedding
    emb_file = emb_dir / f"{img_path.stem}_embedding.json"
    with open(emb_file, "w") as f:
        json.dump(emb.tolist(), f, indent=2)

    print(f"✅ {img_path.name} procesada → {emb_file.name}")

def process_directory(directory: Path):
    if not directory.exists() or not directory.is_dir():
        sys.exit(f"❌ No existe el directorio: {directory}")

    all_images = sorted([f for f in directory.iterdir() if f.suffix.lower() in IMAGE_EXTS])
    if not all_images:
        sys.exit(f"⚠️ No se encontraron imágenes válidas en: {directory}")

    print(f"🔍 Procesando {len(all_images)} imágenes desde: {directory}")
    store_dir = Path("./store")

    for img_path in all_images:
        try:
            tensor = load_and_preprocess(img_path)
            embedding = get_embedding(tensor)
            save_results(img_path, embedding, store_dir)
        except Exception as e:
            print(f"❌ Error al procesar {img_path.name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Uso: python main.py <directorio_de_imagenes>")
        sys.exit(1)

    input_dir = Path(sys.argv[1]).expanduser()
    process_directory(input_dir)
