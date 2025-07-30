import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB2
from tensorflow.keras.applications.efficientnet import preprocess_input as preprocess_efficientnet
from tensorflow.keras.utils import load_img, img_to_array
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean

DATA_DIR = r'C:\workspace\tesis_project\experimentation\tesis_experimentation_v1\model_train_02\similares'
OUTPUT_DIR = r'C:\workspace\tesis_project\experimentation\tesis_experimentation_v1\model_train_02\embeddings'
IMG_SIZE = (224, 224)

def preprocess_image(img_path):
    img = load_img(img_path, target_size=IMG_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_efficientnet(img_array)

def save_embedding(embedding, output_path, filename):
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, f"{os.path.splitext(filename)[0]}.json"), 'w') as f:
        json.dump(embedding, f)

def process_images():
    base_model = EfficientNetB2(weights='imagenet', include_top=False, pooling='avg')
    print(f"\nModelo EfficientNetB2")

    output_path = os.path.join(OUTPUT_DIR, 'arq_efficientnetb2')
    os.makedirs(output_path, exist_ok=True)

    total_images = 0
    successful = 0
    failed = []

    image_files = []
    for root, _, files in os.walk(DATA_DIR):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, f))
    total_images = len(image_files)

    for img_path in tqdm(image_files, desc="Procesando imágenes"):
        filename = os.path.basename(img_path)
        try:
            img_conv = preprocess_image(img_path)
            embedding = base_model.predict(img_conv, verbose=0).flatten().tolist()
            if validate_embedding_format(embedding):
                save_embedding(embedding, output_path, filename)
                successful += 1
            else:
                print(f"Embedding invalido: {filename}")
                failed.append(filename)
        except Exception as e:
            print(f"Error procesando {filename}: {e}")
            failed.append(filename)

    success_rate = (successful / total_images) * 100 if total_images > 0 else 0
    print("\n*** RESULTADOS ***")
    print(f"Total de imagenes procesadas: {total_images}")
    print(f"Embeddings generados correctamente: {successful}")
    print(f"N° Errores: {len(failed)}")
    print(f"Porcentaje de exito: {success_rate:.2f}%")

    if failed:
        print("\Errores en la imagen:")
        for fname in failed:
            print(f"- {fname}")

    validate_embeddings(output_path)

def validate_embedding_format(embedding):
    return (
        isinstance(embedding, list) and
        len(embedding) > 100 and
        all(isinstance(x, (float, int, np.floating)) and np.isfinite(x) for x in embedding)
    )

def load_embedding(path):
    with open(path, 'r') as f:
        return np.array(json.load(f))

def validate_embeddings(output_path):
    print("\n*** VALIDACIÓN SEMANTICA Y EMPIRICA ***")

    ejemplos = sorted([f for f in os.listdir(output_path) if f.endswith('.json')])
    if len(ejemplos) < 3:
        print("No hay suficientes embeddings para validar.")
        return

    emb_a = load_embedding(os.path.join(output_path, ejemplos[0]))
    emb_b = load_embedding(os.path.join(output_path, ejemplos[1]))  # similar
    emb_c = load_embedding(os.path.join(output_path, ejemplos[-1]))  # distinta

    cos_sim_ab = cosine_similarity([emb_a], [emb_b])[0][0]
    cos_sim_ac = cosine_similarity([emb_a], [emb_c])[0][0]

    dist_ab = euclidean(emb_a, emb_b)
    dist_ac = euclidean(emb_a, emb_c)

    print(f"* Similitud de coseno (A vs B similares): {cos_sim_ab:.4f}")
    print(f"* Similitud de coseno (A vs C distintas): {cos_sim_ac:.4f}")
    print(f"* Distancia euclidiana (A vs B similares): {dist_ab:.2f}")
    print(f"* Distancia euclidiana (A vs C distintas): {dist_ac:.2f}")

    if cos_sim_ab > cos_sim_ac and dist_ab < dist_ac:
        print("El embedding capturar diferencias semánticas")
    else:
        print("El embedding no discrimina correctamente entre imágenes.")

if __name__ == "__main__":
    process_images()
