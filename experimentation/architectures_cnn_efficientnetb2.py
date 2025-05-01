import os
import json
import numpy as np
import tensorflow as tf
import time
import wandb
from tensorflow.keras.applications import EfficientNetB2
from tensorflow.keras.applications.efficientnet import preprocess_input as preprocess_efficientnet
from tensorflow.keras.utils import load_img, img_to_array
from tqdm import tqdm

DATA_DIR = './data/train'
OUTPUT_DIR = './output_data'
IMG_SIZE = (260, 260)

# carga y preprocesamiento
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

    wandb.init(
        project="art-similarity",
        name=f"experiment_efficientnetb2",
        config={
            "model": "efficientnetb2",
            "img_size": IMG_SIZE,
            "dataset": DATA_DIR
        }
    )

    output_path = os.path.join(OUTPUT_DIR, f'arq_efficientnetb2')
    os.makedirs(output_path, exist_ok=True)

    for estilo in os.listdir(DATA_DIR):
        estilo_path = os.path.join(DATA_DIR, estilo)
        if not os.path.isdir(estilo_path): continue

        image_files = os.listdir(estilo_path)[:20] 

        for filename in tqdm(image_files, desc=f"Procesando estilo - {estilo}"):
            img_path = os.path.join(estilo_path, filename)

            try:
                img_conv = preprocess_image(img_path)

                start = time.time()

                embedding = base_model.predict(img_conv, verbose=0).flatten().tolist()

                wandb.log({
                    "embedding_mean": np.mean(embedding),
                    "embedding_std": np.std(embedding),
                    "time": time.time() - start
                    })

                save_embedding(embedding, output_path, filename)
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

    wandb.finish()

if __name__ == "__main__":
    process_images()
