import os
import json
import random
import datetime
from sklearn.metrics.pairwise import cosine_similarity

# carga embeddings desde los archivos .json
def load_embeddings(directory):
    return {filename: json.load(open(os.path.join(model_dir, filename), 'r'))
            for model_dir in os.listdir(directory) 
            if os.path.isdir(os.path.join(directory, model_dir))
            for filename in os.listdir(os.path.join(directory, model_dir))
            if filename.endswith('.json')}

def select_random_image(embeddings):
    return random.choice(list(embeddings.items()))

def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def find_most_similar_images(embeddings, reference_embedding, top_n=3):
    return sorted(
        [(image_name, calculate_cosine_similarity(reference_embedding, embedding)) for image_name, embedding in embeddings.items()],
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
    top_similar_images = find_most_similar_images(embeddings, reference_embedding)
    save_results(metric_name, reference_image_name, top_similar_images)

# Cargar embeddings
embeddings = load_embeddings('../output_data')

# Ejecutar el experimento
run_experiment(embeddings)
