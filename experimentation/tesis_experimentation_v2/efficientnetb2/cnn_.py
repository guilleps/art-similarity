import os
import cv2
import json
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
from utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels
)
import logging
from logger_config import setup_logging
import tensorflow
from tensorflow.keras.applications import EfficientNetB2
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image

setup_logging()
logger = logging.getLogger(__name__)

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

def extract_embeddings(image_path, model):
    img = keras_image.load_img(image_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    embedding = model.predict(img_array)
    return embedding[0].tolist()

def process_transformed_folder(transformed_dir, embeddings_output_dir, model):
    os.makedirs(embeddings_output_dir, exist_ok=True)
    for img_name in os.listdir(transformed_dir):
        if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        img_path = os.path.join(transformed_dir, img_name)
        embedding = extract_embeddings(img_path, model)

        name_wo_ext = os.path.splitext(img_name)[0]
        with open(os.path.join(embeddings_output_dir, f"{name_wo_ext}_embedding.json"), "w") as f:
            json.dump(embedding, f)

def run_pipeline(input_dir, transformed_dir, embeddings_dir):
    model = EfficientNetB2(weights='imagenet', include_top=False, pooling='avg')

    image_paths = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    for image_path in tqdm(image_paths, desc="Procesando imágenes"):
        name = os.path.splitext(os.path.basename(image_path))[0]

        # Paso 1: Transformar
        transformed_subfolder = save_transformed_images(image_path, transformed_dir)

        # Paso 2: Extraer embeddings
        embedding_subfolder = os.path.join(embeddings_dir, name)
        process_transformed_folder(transformed_subfolder, embedding_subfolder, model)
