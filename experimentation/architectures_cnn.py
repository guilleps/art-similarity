import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import (
    ResNet50, DenseNet121, EfficientNetV2B0, EfficientNetV2B1
)
from tensorflow.keras.applications.resnet import preprocess_input as preprocess_resnet
from tensorflow.keras.applications.densenet import preprocess_input as preprocess_densenet
from tensorflow.keras.applications.efficientnet import preprocess_input as preprocess_efficientnet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.utils import load_img, img_to_array
from tqdm import tqdm

DATA_DIR = './data/train'
OUTPUT_DIR = './output_data'
IMG_SIZE = (224, 224)

# carga y preprocesamiento
def preprocess_image(img_path, preprocess_func):
    img = load_img(img_path, target_size=IMG_SIZE)
    return preprocess_func(np.expand_dims(img_to_array(img), axis=0))

def save_embedding(embedding, output_path, filename):
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, f"{os.path.splitext(filename)[0]}.json"), 'w') as f:
        json.dump(embedding, f)

def load_and_preprocess_image(img_path, preprocess_func):
    img = load_img(img_path, target_size=IMG_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_func(img_array)

# json de modelos definidos a usar
MODELS = {
    'resnet': (ResNet50(weights='imagenet', include_top=False, pooling='avg'), preprocess_resnet),
    'densenet': (DenseNet121(weights='imagenet', include_top=False, pooling='avg'), preprocess_densenet),
    'efficientnetv2b0': (EfficientNetV2B0(weights='imagenet', include_top=False, pooling='avg'), preprocess_efficientnet),
    'efficientnetv2b1': (EfficientNetV2B1(weights='imagenet', include_top=False, pooling='avg'), preprocess_efficientnet),
}

def process_images():
    for model_name, (base_model, preprocess_func) in MODELS.items():
        print(f"\nProcesando modelo: {model_name}")

        output_path = os.path.join(OUTPUT_DIR, f'arq_{model_name}')
        os.makedirs(output_path, exist_ok=True)

        for estilo in os.listdir(DATA_DIR):
            estilo_path = os.path.join(DATA_DIR, estilo)
            if not os.path.isdir(estilo_path): continue

            image_files = os.listdir(estilo_path)[:10] 

            for filename in tqdm(image_files, desc=f"Procesando estilo - {estilo}"):
                img_path = os.path.join(estilo_path, filename)

                try:
                    img_tensor = preprocess_image(img_path, preprocess_func)
                    embedding = base_model.predict(img_tensor, verbose=0).flatten().tolist()
                    save_embedding(embedding, output_path, filename)
                except Exception as e:
                    print(f"Error procesando {filename}: {e}")

if __name__ == "__main__":
    process_images()
