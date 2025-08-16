import os
from cnn_ import run_pipeline
from cosine_similarity import compare_all_embeddings
import logging
from logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def find_image_folders(base_folder):
    image_folders = []
    for root, dirs, files in os.walk(base_folder):
        if any(file.lower().endswith(('.png', '.jpg', '.jpeg')) for file in files):
            image_folders.append(root)
    return image_folders

def main():
    base_folder = r"C:\workspace\tesis_project\tesis_experimentation_v4\clip-net\images\1"
    embeddings_dir = os.path.join(base_folder, "embeddings")
    transformed_dir = os.path.join(base_folder, "transformed_images")
    output_json_path = os.path.join(embeddings_dir, "resultados_similitud.json")
    
    # Ejecucion de pipeline de transformaciones y extracción de embeddings
    logger.info("Inicio del pipeline...")
    run_pipeline(base_folder, transformed_dir, embeddings_dir)

    logger.info("Buscando carpetas con embeddings...")
    embedding_folders = [
        os.path.join(embeddings_dir, folder) 
        for folder in os.listdir(embeddings_dir) 
        if os.path.isdir(os.path.join(embeddings_dir, folder))
    ]

    # Paso 3: Comparar todos los pares de embeddings (evitando comparar consigo mismo)
    logger.info("Comparando similitudes...")
    for i in range(len(embedding_folders)):
        for j in range(i + 1, len(embedding_folders)):
            compare_all_embeddings(
                embedding_folders[i], 
                embedding_folders[j], 
                output_json_path
            )
    
    logger.info("Pipeline completado")

if __name__ == "__main__":
    main()
