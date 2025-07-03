import glob
import json
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

paths = glob.glob("*.json")

vectors = []

for path in paths:
    with open(path, 'r') as f:
        data = json.load(f)
        vectors.append(data)

X = np.array(vectors)
print(f"Forma del array: {X.shape}")

pca_full = PCA()
pca_full.fit(X)

cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)

plt.figure()
plt.plot(cumulative_variance, marker='o')
plt.axhline(y=0.95, color='r', linestyle='--', label='95% --')
plt.xlabel('n° de componentes')
plt.ylabel('varianza acumulada')
plt.title('(PCA)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

n_components_95 = np.argmax(cumulative_variance >= 0.95) + 1 # cuantos componentes realmente se necesitan?
print(f"N° Componentes {n_components_95} necesarios para su representatividad")

pca_2d = PCA(n_components=2) # para visualizacion
X_pca = pca_2d.fit_transform(X)

plt.figure()
plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.7, edgecolors='k')
plt.title('Visualización PCA de Vectores en 2D')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.grid(True)
plt.tight_layout()
plt.show()
