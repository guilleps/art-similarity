import os
import json
from sklearn.metrics.pairwise import cosine_similarity

# Cargar todos los embeddings de una carpeta
def load_embeddings_from_folder(folder_path):
    embeddings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith("_embedding.json"):
            with open(os.path.join(folder_path, filename), "r") as f:
                embeddings[filename] = json.load(f)
    return embeddings

# Calcular similitud coseno entre dos vectores
def compare_embeddings(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# Extraer la clave de transformación a partir del nombre de archivo
def get_transform_key(filename):
    parts = filename.split("_embedding")[0].split("_")
    if "hsv" in filename:
        return f"hsv_{parts[-1]}"
    elif "color_map" in filename:
        return "heat_color_map"
    elif "contrast" in filename:
        return "contrast"
    elif "texture" in filename:
        return "texture"
    else:
        return "unknown"

# Comparar todos los embeddings entre dos carpetas
def compare_all_embeddings(image1_folder, image2_folder, output_json_path):
    image1_embeddings = load_embeddings_from_folder(image1_folder)
    image2_embeddings = load_embeddings_from_folder(image2_folder)

    results = {}

    for key1, emb1 in image1_embeddings.items():
        transform_key = get_transform_key(key1)

        for key2, emb2 in image2_embeddings.items():
            if get_transform_key(key2) == transform_key:
                similarity = compare_embeddings(emb1, emb2)
                results[transform_key] = {
                    "files": [key1, key2],
                    "similarity": round(similarity, 4)
                }

    with open(output_json_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Comparaciones guardadas en: {output_json_path}")

# Ejecutar comparación
def run_comparisons():
    image1_folder = r"C:\workspace\tesis_project\experimentation\tesis_experimentation_v2\images\5\embeddings\albert-julius-olsson_a-song-of-the-sea"
    image2_folder = r"C:\workspace\tesis_project\experimentation\tesis_experimentation_v2\images\5\embeddings\albert-julius-olsson_storm-cloud"
    output_json_path = r"C:\workspace\tesis_project\experimentation\tesis_experimentation_v2\images\5\embeddings\resultados_similitud.json"

    compare_all_embeddings(image1_folder, image2_folder, output_json_path)

if __name__ == "__main__":
    run_comparisons()
