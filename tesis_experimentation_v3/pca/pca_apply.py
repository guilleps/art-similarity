import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Ruta a tu carpeta de embeddings
EMBEDDING_DIR = "embeddings"
OUTPUT_DIR = "embeddings_pca"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Paso 1: Cargar todos los embeddings en una matriz
embeddings = []
file_paths = []

for file in os.listdir(EMBEDDING_DIR):
    if file.endswith("_embedding.json"):
        path = os.path.join(EMBEDDING_DIR, file)
        with open(path, "r") as f:
            emb = json.load(f)
            embeddings.append(emb)
            file_paths.append(path)

X = np.array(embeddings)

# Paso 2: Normalizar (estandarizar) antes de PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA().fit(X_scaled)
explained_variance = np.cumsum(pca.explained_variance_ratio_)

# Paso 4: Visualización para elegir número óptimo de componentes
plt.figure(figsize=(10, 6))
plt.plot(np.arange(1, len(explained_variance)+1), explained_variance, marker='o')
plt.title("Varianza explicada acumulada (PCA)")
plt.xlabel("Número de componentes")
plt.ylabel("Varianza explicada acumulada")
plt.grid(True)
plt.axhline(0.95, color='r', linestyle='--', label='95% umbral')
plt.legend()
plt.tight_layout()
plt.show()
