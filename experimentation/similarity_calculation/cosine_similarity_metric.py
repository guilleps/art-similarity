import os
import json
import random
import datetime
import wandb
from sklearn.metrics.pairwise import cosine_similarity

wandb.init(
    project="art-similarity-metrics",
    name="experiment_cosine_similarity",
    config={
        "metric": "cosine",
        "top_k": 3
    }
)

# carga embeddings desde los archivos .json
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
    return random.choice(list(embeddings.items()))

def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def find_most_similar_images(embeddings, reference_embedding, reference_image_name, top_n=3):
    return sorted(
        [(image_name, calculate_cosine_similarity(reference_embedding, embedding)) 
         for image_name, embedding in embeddings.items() if image_name != reference_image_name],  # Excluye la imagen de referencia
        key=lambda x: x[1], reverse=True
    )[:top_n]

def save_results(metric_name, reference_image_name, top_similar_images):
    results_dir = os.path.join('./logs', metric_name)
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    result_file_path = os.path.join(results_dir, f"comparison_{timestamp}.json")
    
    result_data = {
        "reference_image": reference_image_name,
        "top_similar_images": [{"image_name": img[0], "similarity": img[1]} for img in top_similar_images]
    }

    with open(result_file_path, 'w') as f:
        json.dump(result_data, f, indent=4)
    
    print(f"Resultados guardados en {result_file_path}")

def run_experiment(embeddings, metric_name="cosine_similarity"):
    reference_image_name, reference_embedding = select_random_image(embeddings)
    top_similar_images = find_most_similar_images(embeddings, reference_embedding, reference_image_name)
    save_results(metric_name, reference_image_name, top_similar_images)

    return reference_image_name, top_similar_images

embeddings = load_embeddings('../output_data')
reference_image_name, top_similar_images = run_experiment(embeddings)

wandb.log({
    "top1_score": top_similar_images[0][1],
    "top2_score": top_similar_images[1][1],
    "top3_score": top_similar_images[2][1]
})

wandb.finish()
