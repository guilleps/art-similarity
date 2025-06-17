import os
from cnn_ import run_pipeline
from cosine_similarity import compare_all_embeddings
import logging
from logger_config import setup_logging
from similarity_metrics import compare_all_embeddings_with_metrics

setup_logging()
logger = logging.getLogger(__name__)

def main():
    # Define las rutas base que usas en tus scripts
    embeddings_base_folder = r"C:\workspace\tesis_project\experimentation\tesis_experimentation_v2\efficientnetb2\images\2\embeddings"
    input_images_folder = r"C:\workspace\tesis_project\experimentation\tesis_experimentation_v2\efficientnetb2\images\2"
    
    # Ejecucion de pipeline de transformaciones y extracción de embeddings
    logger.info("Inicio del pipeline...")

    transformed_dir = os.path.join(input_images_folder, "transformed_images")
    embeddings_dir = os.path.join(input_images_folder, "embeddings")
    logger.info("Transformando y organizandos vectores multidimensionales...")
    run_pipeline(input_images_folder, transformed_dir, embeddings_dir)
    
    # Comparación y generación del JSON con resultados
    image1_folder = os.path.join(embeddings_base_folder, "antoine-blanchard_boulevard-de-la-madeleine-9")
    image2_folder = os.path.join(embeddings_base_folder, "armando-montaner-valdueza_portrait-of-spanish-woman")
    output_json_path = os.path.join(embeddings_base_folder, "resultados_similitud.json")
    
    logger.info("Analizando y obteniendo comparación de similitudes...")
    compare_all_embeddings_with_metrics(image1_folder, image2_folder, output_json_path)
    
    logger.info("Acabé... Fin del pipeline")

if __name__ == "__main__":
    main()
