Perfecto. Vamos a ver **cómo extraer y comparar embeddings** paso a paso después de entrenar tu modelo con fine-tuning. Esto es clave si quieres usar tus embeddings para análisis, visualización o tareas como detección de similitud entre obras de arte.

---

## ✅ 1. Extraer embeddings con tu modelo entrenado

Supongamos que ya entrenaste tu modelo y la capa de embeddings se llama `"embedding"` (como en la estrategia anterior):

```python
from tensorflow.keras.models import Model

# Crea un nuevo modelo que termina en la capa de embeddings
embedding_model = Model(inputs=model.input,
                        outputs=model.get_layer('embedding').output)

# Preprocesa tus imágenes (puede ser una sola imagen o lote)
from tensorflow.keras.preprocessing import image
import numpy as np

img_path = 'ruta/a/mi_imagen.jpg'
img = image.load_img(img_path, target_size=(256, 256))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Extrae el embedding
embedding_vector = embedding_model.predict(img_array)  # shape: (1, 128)
```

---

## ✅ 2. Comparar embeddings entre imágenes

Puedes comparar dos imágenes usando **métricas de similitud**. Las más comunes son:

### 📌 Cosine Similarity

```python
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(embedding1, embedding2)  # rango: -1 a 1
```

### 📌 Distancia Euclidiana

```python
from scipy.spatial.distance import euclidean

dist = euclidean(embedding1.flatten(), embedding2.flatten())  # menor = más similares
```

---

## ✅ 3. Evaluar similitudes en lote

Si tienes una galería de embeddings, puedes comparar todos contra uno:

```python
query_embedding = embedding_model.predict(query_image)

# Supón que gallery_embeddings es de shape (n, 128)
from scipy.spatial.distance import cdist
distances = cdist(query_embedding, gallery_embeddings, metric='cosine')  # shape (1, n)
```

Luego puedes ordenar los resultados:

```python
indices_ordenados = distances[0].argsort()  # más similares primero
```

---

## ✅ 4. Visualización con t-SNE o PCA (opcional)

Esto te permite **ver gráficamente** qué tan bien el modelo separa los estilos.

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

tsne = TSNE(n_components=2, random_state=42)
X_2d = tsne.fit_transform(gallery_embeddings)

plt.scatter(X_2d[:, 0], X_2d[:, 1], c=gallery_labels, cmap='tab10')
plt.title("Visualización de Embeddings con t-SNE")
plt.show()
```

---

¿Quieres que te dé un Colab listo con este flujo de comparación visual? ¿O prefieres integrar esta lógica en tu app backend o frontend?
