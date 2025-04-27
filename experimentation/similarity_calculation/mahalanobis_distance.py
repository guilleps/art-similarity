import os
import json
import random
import numpy as np
from scipy.spatial.distance import mahalanobis
from numpy.linalg import inv
import datetime
import wandb

wandb.init(
    project="art-similarity-metrics",
    name="experiment_mahalanobis_similarity",
    config={
        "metric": "mahalanobis",
        "top_k": 3
    }
)

def load_embeddings(directory):
    embeddings = {}
    for model_dir in os.listdir(directory):
        model_path = os.path.join(directory, model_dir)
        if os.path.isdir(model_path):
            for filename in os.listdir(model_path):
                if filename.endswith('.json'):
                    with open(os.path.join(model_path, filename), 'r') as f:
                        embeddings[filename] = json.load(f)
    return embeddings

def select_random_image(embeddings):
    image_name = random.choice(list(embeddings.keys()))
    return image_name, embeddings[image_name]

def mahalanobis_distance(embedding1, embedding2, inv_cov_matrix):
    diff = np.array(embedding1) - np.array(embedding2)
    return mahalanobis(diff, np.zeros(len(diff)), inv_cov_matrix)

def find_similar_images(embeddings, reference_image_name, reference_embedding, top_n=3):
    all_embeddings = np.array(list(embeddings.values()))
    inv_cov_matrix = inv(np.cov(all_embeddings, rowvar=False))

    similarities = [
        (image_name, mahalanobis_distance(reference_embedding, embedding, inv_cov_matrix))
        for image_name, embedding in embeddings.items() if image_name != reference_image_name
    ]
    
    return sorted(similarities, key=lambda x: x[1])[:top_n]

def create_directory(metric_name):
    dir_path = os.path.join('./logs', metric_name)
    os.makedirs(dir_path, exist_ok=True)  
    return dir_path

def save_results(metric_name, reference_image_name, top_similar_images):
    results_dir = create_directory(metric_name)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    result_file_path = os.path.join(results_dir, f"comparison_{timestamp}.json")

    result_data = {
        "reference_image": reference_image_name,
        "top_similar_images": [{"image_name": img[0], "similarity": img[1]} for img in top_similar_images]
    }

    with open(result_file_path, 'w') as f:
        json.dump(result_data, f, indent=4)
    
    print(f"Resultados guardados en {result_file_path}")

def run_mahalanobis_experiment(embeddings):
    reference_image_name, reference_embedding = select_random_image(embeddings)
    top_similar_images = find_similar_images(embeddings, reference_image_name, reference_embedding)
    save_results("mahalanobis_distance", reference_image_name, top_similar_images)

    return reference_image_name, top_similar_images

embeddings = load_embeddings('../output_data')
reference_image_name, top_similar_images = run_mahalanobis_experiment(embeddings)


wandb.log({
    "reference_image": reference_image_name,
    "top1_score": top_similar_images[0][1],
    "top2_score": top_similar_images[1][1],
    "top3_score": top_similar_images[2][1],
})

table = wandb.Table(columns=["Imagen", "Similitud"])
for image_name, score in top_similar_images:
    table.add_data(image_name, score)

wandb.log({"Top similitud": table})

wandb.finish()
