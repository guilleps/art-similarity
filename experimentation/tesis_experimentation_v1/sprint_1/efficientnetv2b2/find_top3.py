import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import (
    EfficientNetB2,
    preprocess_input,
)
import matplotlib.pyplot as plt
from PIL import Image

MODEL = EfficientNetB2(include_top=False, weights="imagenet", pooling="avg")
EMB_DIM = MODEL.output_shape[-1]  # 1280
IMAGE_SIZE = (224, 224)

def load_and_preprocess(img_path: Path) -> np.ndarray:
    img = image.load_img(img_path, target_size=IMAGE_SIZE)
    x = image.img_to_array(img)
    x = np.expand_dims(x, 0)
    return preprocess_input(x)

def get_embedding(img_path: Path) -> np.ndarray:
    tensor = load_and_preprocess(img_path)
    return MODEL(tensor).numpy().squeeze()

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def load_store_embeddings(emb_dir: Path):
    embeddings = {}
    for json_path in emb_dir.glob("*_embedding.json"):
        with open(json_path) as f:
            embeddings[json_path.stem.replace("_embedding", "")] = np.array(json.load(f), dtype=np.float32)
    if not embeddings:
        raise SystemExit(f"⚠️ No se encontraron embeddings en {emb_dir}")
    return embeddings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=Path, help="Imagen de consulta")
    parser.add_argument("--store", type=Path, default=Path("./store"), help="Carpeta base con /images y /embeddings")
    args = parser.parse_args()

    query_img = args.query.expanduser()
    if not query_img.exists():
        raise SystemExit(f"❌ Imagen no encontrada: {query_img}")

    store_dir = args.store.expanduser()
    emb_dir = store_dir / "embeddings"
    img_dir = store_dir / "images"

    query_emb = get_embedding(query_img)

    db_embeddings = load_store_embeddings(emb_dir)

    scores = []
    for name, emb in db_embeddings.items():
        sim = cosine_sim(query_emb, emb)
        scores.append((name, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    top_n = scores[:4]

    # ─── Mostrar resultados ───
    print("\nTop-3 más similares:")
    for rank, (name, sim) in enumerate(top_n, 1):
        print(f"{rank}. {name}  —  similitud: {sim:.4f}")

    # ─── Mostrar imágenes con matplotlib ───
    fig, axes = plt.subplots(1, 5, figsize=(14, 4))
    axes[0].imshow(Image.open(query_img))
    axes[0].set_title("Consulta")
    axes[0].axis("off")

    for ax, (name, sim) in zip(axes[1:], top_n):
        img_path = img_dir / f"{name}.jpg"
        ax.imshow(Image.open(img_path))
        ax.set_title(f"{sim * 100:.2f}%")
        ax.axis("off")

    plt.suptitle("Top-3 similitud coseno (EfficientNetB2)", fontsize=14)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
