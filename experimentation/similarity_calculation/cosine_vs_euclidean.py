import os
import json
import random
import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
import wandb

config = {
    "metrics": ["cosine_similarity", "euclidean_distance"],
    "top_k": 3,
}

wandb.init(
    project="art-similarity-metrics",
    name="experiment_cosine_vs_euclidean",
    config=config
)

name_architecture = 'arq_efficientnetb7'
data = os.path.join('../output_data', name_architecture)
output_directory = './logs'

# carga embeddings desde los archivos .json
def load_embeddings(directory):
    embeddings = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                embeddings[filename] = json.load(f)
    return embeddings

def select_random_image(embeddings):
    image_name = random.choice(list(embeddings.keys()))
    return image_name, embeddings[image_name]

def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def calculate_euclidean_distance(embedding1, embedding2):
    return euclidean(embedding1, embedding2)

def find_most_similar_images_cosine(embeddings, reference_embedding, reference_image_name, top_n=3):
    similarities = [
        (image_name, calculate_cosine_similarity(reference_embedding, embedding))
        for image_name, embedding in embeddings.items()
        if image_name != reference_image_name
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)  # mayor = mas similar
    return similarities[:top_n]

def find_most_similar_images_euclidean(embeddings, reference_embedding, reference_image_name, top_n=3):
    similarities = [
        (image_name, calculate_euclidean_distance(reference_embedding, embedding))
        for image_name, embedding in embeddings.items()
        if image_name != reference_image_name
    ]
    similarities.sort(key=lambda x: x[1])  # menor = mas similar
    return similarities[:top_n]

def save_results(reference_image_name, cosine_results, euclidean_results):
    result_data = {
        "reference_image": reference_image_name,
        "architecture": name_architecture,
        "cosine_top_similar_images": [{"image_name": img[0], "similarity": img[1]} for img in cosine_results],
        "euclidean_top_similar_images": [{"image_name": img[0], "distance": img[1]} for img in euclidean_results]
    }

    results_dir = os.path.join(output_directory, 'cosine_vs_euclidean')
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    result_file_path = os.path.join(results_dir, f"comparison_{timestamp}.json")

    with open(result_file_path, 'w') as f:
        json.dump(result_data, f, indent=4)

    print(f"Resultados guardados en {result_file_path}")

def run_experiment(embeddings, metric_name="cosine_similarity"):
    reference_image_name, reference_embedding = select_random_image(embeddings)
    
    cosine_top = find_most_similar_images_cosine(embeddings, reference_embedding, reference_image_name)
    euclidean_top = find_most_similar_images_euclidean(embeddings, reference_embedding, reference_image_name)

    save_results(reference_image_name, cosine_top, euclidean_top)

    wandb.log({
        "reference_image": reference_image_name,
        "cosine_top1_score": cosine_top[0][1],
        "cosine_top2_score": cosine_top[1][1],
        "cosine_top3_score": cosine_top[2][1],
        "euclidean_top1_distance": euclidean_top[0][1],
        "euclidean_top2_distance": euclidean_top[1][1],
        "euclidean_top3_distance": euclidean_top[2][1],
    })

    cosine_table = wandb.Table(columns=["Imagen", "Cosine Similarity"])
    for image_name, score in cosine_top:
        cosine_table.add_data(image_name, score)
    
    euclidean_table = wandb.Table(columns=["Imagen", "Euclidean Distance"])
    for image_name, distance in euclidean_top:
        euclidean_table.add_data(image_name, distance)
    
    wandb.log({
        "Cosine Top Similarities": cosine_table,
        "Euclidean Top Distances": euclidean_table
    })

    return reference_image_name, cosine_top, euclidean_top

embeddings = load_embeddings(data)
reference_image_name, cosine_top, euclidean_top = run_experiment(embeddings)

wandb.finish()
