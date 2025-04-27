import os
import json
import random
import numpy as np
from scipy.spatial.distance import euclidean
import datetime
import wandb

wandb.init(
    project="art-similarity-metrics",
    name="experiment_euclidean_similarity",
    config={
        "metric": "euclidean",
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
                    filepath = os.path.join(model_path, filename)
                    with open(filepath, 'r') as f:
                        embeddings[filename] = json.load(f) 
    return embeddings

def select_random_image(embeddings):
    image_name = random.choice(list(embeddings.keys())) 
    return image_name, embeddings[image_name]  

def create_results_directory(metric_name):
    dir_path = os.path.join('./logs', metric_name)
    os.makedirs(dir_path, exist_ok=True)  
    return dir_path

def save_comparison_result(metric_name, reference_image_name, top_similar_images):
    results_dir = create_results_directory(metric_name)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    result_file_path = os.path.join(results_dir, f"comparison_{timestamp}.json")
    
    result_data = {
        "reference_image": reference_image_name,
        "top_similar_images": [{"image_name": img[0], "similarity": img[1]} for img in top_similar_images]
    }

    with open(result_file_path, 'w') as f:
        json.dump(result_data, f, indent=4)
    
    print(f"Resultados guardados en {result_file_path}")

def calculate_euclidean_distance(embedding1, embedding2):
    return euclidean(embedding1, embedding2)

def find_most_similar_images(embeddings, reference_image_name, reference_embedding, top_n=3):
    similarities = []
    for image_name, embedding in embeddings.items():
        if image_name != reference_image_name:  
            similarity = calculate_euclidean_distance(reference_embedding, embedding)
            similarities.append((image_name, similarity))
    
    similarities.sort(key=lambda x: x[1])  
    return similarities[:top_n]

def run_euclidean_experiment(embeddings):
    reference_image_name, reference_embedding = select_random_image(embeddings)
    top_similar_images = find_most_similar_images(embeddings, reference_image_name, reference_embedding, top_n=3)
    save_comparison_result("euclidean_distance", reference_image_name, top_similar_images)

    return reference_image_name, top_similar_images

embeddings = load_embeddings('../output_data')
reference_image_name, top_similar_images = run_euclidean_experiment(embeddings)

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
