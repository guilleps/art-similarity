import os
import json
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel
from tqdm import tqdm

# Función para cargar embeddings de los archivos JSON
def load_embeddings_from_folder(folder_path):
    embeddings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith("_embedding.json"):
            with open(os.path.join(folder_path, filename), "r") as f:
                embeddings[filename] = json.load(f)
    return embeddings

# Función para comparar similitud coseno entre dos embeddings
def compare_embeddings(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# Función para comparar los embeddings 'heatmap' de dos imágenes
def compare_heatmap_embeddings(image1_folder, image2_folder, embeddings_base_folder):
    # Cargar los embeddings de los filtros
    image1_embeddings = load_embeddings_from_folder(image1_folder)
    image2_embeddings = load_embeddings_from_folder(image2_folder)

    # Asegúrate de que el nombre del filtro sea "color_map_embedding.json"
    image1_heatmap = image1_embeddings.get("antoine-blanchard_boulevard-de-la-madeleine-2_color_map_embedding.json")
    image2_heatmap = image2_embeddings.get("antoine-blanchard_boulevard-de-la-madeleine-9_color_map_embedding.json")

    if not image1_heatmap or not image2_heatmap:
        print("No se encontraron los embeddings de heatmap para alguna de las imágenes.")
        return

    # Calcular similitud coseno entre los embeddings de heatmap
    similarity = compare_embeddings(image1_heatmap, image2_heatmap)
    print(f"Similitud coseno entre 'heatmap' de imagen 1 y imagen 2: {similarity:.4f}")
    return similarity

# Función principal para realizar la comparación entre las dos carpetas de imágenes
def run_comparisons():    
    # Ubicaciones de los embeddings de las dos imágenes (las rutas completas)
    image1_folder = "C:/workspace/deep_learning/filters/images/1/embeddings/antoine-blanchard_boulevard-de-la-madeleine-2"
    image2_folder = "C:/workspace/deep_learning/filters/images/1/embeddings/antoine-blanchard_boulevard-de-la-madeleine-9"

    # Comparar los embeddings de heatmap entre las dos imágenes
    compare_heatmap_embeddings(image1_folder, image2_folder, "C:/workspace/deep_learning/filters/images/1/embeddings")

if __name__ == "__main__":
    run_comparisons()


