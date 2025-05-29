import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

def load_embeddings_from_folder(folder_path):
    embeddings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith("_embedding.json"):
            with open(os.path.join(folder_path, filename), "r") as f:
                embeddings[filename] = json.load(f)
    return embeddings

def compare_embeddings(embeddings1, embeddings2):
    """ Calcula la similitud coseno entre dos conjuntos de embeddings """
    all_embeddings1 = list(embeddings1.values())
    all_embeddings2 = list(embeddings2.values())
    
    # Calcula similitud coseno
    cosine_sim_matrix = cosine_similarity(all_embeddings1, all_embeddings2)
    
    return cosine_sim_matrix

def process_and_compare(image_name, transformed_dir, embeddings_base_folder):
    # Directorios de embeddings
    emb_image_dir = os.path.join(embeddings_base_folder, image_name)
    
    # Cargar los embeddings generados por CLIP para cada filtro de la imagen transformada
    embeddings = load_embeddings_from_folder(emb_image_dir)
    
    # Crear un diccionario para almacenar los resultados
    similarity_results = {}
    
    # Comparar cada filtro con cada otro filtro
    for filter1, emb1 in embeddings.items():
        similarity_results[filter1] = {}
        for filter2, emb2 in embeddings.items():
            if filter1 != filter2:
                similarity = cosine_similarity([emb1], [emb2])[0][0]
                similarity_results[filter1][filter2] = similarity
    
    # Guardar los resultados de similitud en un archivo
    similarity_file = os.path.join(emb_image_dir, f"{image_name}_similarity_results.json")
    with open(similarity_file, "w") as f:
        json.dump(similarity_results, f, indent=4)
    
    print(f"Similitud entre filtros guardada en: {similarity_file}")
    return similarity_results

def run_comparisons(embeddings_base_folder):
    # Obtener todas las subcarpetas (por cada imagen)
    for image_folder in os.listdir(embeddings_base_folder):
        image_dir = os.path.join(embeddings_base_folder, image_folder)
        if os.path.isdir(image_dir):
            print(f"Comparando similitud para: {image_folder}")
            process_and_compare(image_folder, image_dir, embeddings_base_folder)
            
if __name__ == "__main__":
    # Carpeta base donde están los embeddings generados
    embeddings_base_folder = "embeddings"
    
    # Ejecutar la comparación de similitudes
    run_comparisons(embeddings_base_folder)
