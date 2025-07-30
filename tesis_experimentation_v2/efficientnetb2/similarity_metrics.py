import os
import json
import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cityblock, euclidean, mahalanobis

from logger_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

def load_embeddings_from_folder(folder_path):
    embeddings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith("_embedding.json"):
            with open(os.path.join(folder_path, filename), "r") as f:
                embeddings[filename] = json.load(f)
    logger.info(f"Se cargaron {len(embeddings)} embeddings desde {folder_path}")
    return embeddings

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
    
def compare_all_embeddings_with_metrics(folder1, folder2, output_path):
    emb1 = load_embeddings_from_folder(folder1)
    emb2 = load_embeddings_from_folder(folder2)

    results = {}

    for key1, vec1 in emb1.items():
        transform_key = get_transform_key(key1)

        for key2, vec2 in emb2.items():
            if get_transform_key(key2) != transform_key:
                continue

            v1 = np.array(vec1)
            v2 = np.array(vec2)

            cosine = round(float(cosine_similarity([v1], [v2])[0][0]), 4)
            euc = round(euclidean(v1, v2), 4)
            man = round(cityblock(v1, v2), 4)

            try:
                cov = np.cov(np.stack([v1, v2]).T)
                inv_cov = np.linalg.pinv(cov)
                maha = round(mahalanobis(v1, v2, inv_cov), 4)
            except:
                maha = "undefined"

            results[transform_key] = {
                "files": [key1, key2],
                "cosine_similarity": cosine,
                "euclidean_distance": euc,
                "manhattan_distance": man,
                "mahalanobis_distance": maha
            }

    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    logger.info(f"Métricas múltiples guardadas en: {output_path}")
    