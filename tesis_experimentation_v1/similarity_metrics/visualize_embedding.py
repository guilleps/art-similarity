import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm
from math import acos, degrees

def load_embedding(path):
    with open(path, 'r') as f:
        return np.array(json.load(f))

embedding1_path = "C:/workspace/output_data/arq_efficientnetb2/Abercrombie_1954_Figure_coming_out_of_a_tree.json"
embedding2_path = "C:/workspace/output_data/arq_efficientnetb2/abbott-handerson-thayer_the-angel-1903.json"

embedding1 = load_embedding(embedding1_path)
embedding2 = load_embedding(embedding2_path)
embeddings = np.array([embedding1, embedding2])
labels = ['balcic-fountain', 'still-life-with-apples']

cos_sim = cosine_similarity([embedding1], [embedding2])[0][0]
angle_rad = acos(np.clip(cos_sim, -1.0, 1.0))
angle_deg = degrees(angle_rad)

print(f"🔍 Similitud del coseno: {cos_sim:.4f}")
print(f"📐 Ángulo entre vectores: {angle_deg:.2f}°")

def plot_quiver(embeddings, labels):
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(embeddings)

    origin = np.zeros((2, 2))
    plt.figure(figsize=(6, 6))
    plt.quiver(*origin, reduced[:, 0], reduced[:, 1], angles='xy', scale_units='xy', scale=1, color=['red', 'blue'])
    for i, label in enumerate(labels):
        plt.text(reduced[i, 0]*1.1, reduced[i, 1]*1.1, label, fontsize=12)
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.title("🔁 Comparación de Embeddings con Quiver Plot")
    plt.show()


def plot_cosine_heatmap(embeddings, labels):
    sim_matrix = cosine_similarity(embeddings)
    plt.figure(figsize=(4, 3))
    sns.heatmap(sim_matrix, xticklabels=labels, yticklabels=labels, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("🔥 Matriz de Similitud Coseno")
    plt.show()

# ---------- USO ----------
plot_quiver(embeddings, labels)
plot_cosine_heatmap(embeddings, labels)
