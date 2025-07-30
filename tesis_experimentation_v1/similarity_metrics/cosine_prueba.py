import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_embedding(path):
    with open(path, 'r') as f:
        return np.array(json.load(f))

def find_most_similar(input_path, folder_path):
    input_filename = os.path.basename(input_path)
    input_embedding = load_embedding(input_path).reshape(1, -1)
    max_sim = -1
    most_similar_file = None

    for file in os.listdir(folder_path):
        if not file.endswith('.json'):
            continue
        if file == input_filename:
            continue

        file_path = os.path.join(folder_path, file)

        try:
            candidate_embedding = load_embedding(file_path).reshape(1, -1)
            sim = cosine_similarity(input_embedding, candidate_embedding)[0][0]
            if sim > max_sim:
                max_sim = sim
                most_similar_file = file
        except Exception as e:
            print(f"[!] Error con {file}: {e}")

    return {
        "input_file": input_filename,
        "most_similar_file": most_similar_file,
        "similarity_score": round(max_sim, 4)
    }

# ---------- USO ----------
input_embedding_path = "C:/workspace/output_data/arq_efficientnetb2/Abercrombie_1954_Figure_coming_out_of_a_tree.json"
embedding_folder_path = "C:/workspace/output_data/arq_efficientnetb2"

result = find_most_similar(input_embedding_path, embedding_folder_path)
print("📁 Comparación completada:")
print("Input:", result["input_file"])
print("Más parecido:", result["most_similar_file"])
print("Similitud:", result["similarity_score"])
