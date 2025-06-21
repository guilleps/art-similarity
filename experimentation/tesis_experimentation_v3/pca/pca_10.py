import os
import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Ruta donde están tus embeddings originales (en formato JSON de listas)
INPUT_DIR = "embeddings"
OUTPUT_DIR = "embeddings_pca"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar todos los embeddings
embeddings = []
file_paths = []

for filename in os.listdir(INPUT_DIR):
    if filename.endswith("_embedding.json"):
        with open(os.path.join(INPUT_DIR, filename), "r") as f:
            vector = json.load(f)
            embeddings.append(vector)
            file_paths.append(filename)

X = np.array(embeddings)

# Normalizar (media 0, varianza 1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar PCA global con 10 componentes
pca = PCA(n_components=21)
X_pca = pca.fit_transform(X_scaled)

# Guardar nuevos embeddings reducidos
for reduced_vec, filename in zip(X_pca, file_paths):
    output_path = os.path.join(OUTPUT_DIR, filename.replace("_embedding.json", "_pca10.json"))
    with open(output_path, "w") as f:
        json.dump(reduced_vec.tolist(), f)

print(f"✅ PCA global aplicado con éxito. {len(file_paths)} embeddings reducidos a 10D y guardados en '{OUTPUT_DIR}'.")
