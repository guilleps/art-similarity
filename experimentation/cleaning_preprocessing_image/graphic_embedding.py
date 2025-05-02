import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def load_embedding(json_path):
    with open(json_path, 'r') as f:
        return np.array(json.load(f))

def load_embeddings(folder_path, limit=None):
    embeddings = []
    labels = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            try:
                embedding = load_embedding(os.path.join(folder_path, file))
                embeddings.append(embedding)
                labels.append(os.path.splitext(file)[0])
                if limit and len(embeddings) >= limit:
                    break
            except Exception as e:
                print(f"❌ Error en {file}: {e}")
    return np.array(embeddings), labels


embedding_folder_path = "C:/workspace/output_data/arq_efficientnetb2"
embeddings, labels = load_embeddings(embedding_folder_path)
