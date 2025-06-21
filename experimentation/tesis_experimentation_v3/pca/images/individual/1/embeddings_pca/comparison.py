import os
import json
from sklearn.metrics.pairwise import cosine_similarity

# Rutas a las carpetas de embeddings PCA por imagen
EMB_DIR_1 = "1"
EMB_DIR_2 = "2"

# Cargar todos los embeddings en diccionarios por transformación
def load_embeddings(folder_path):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith("_pca10.json"):
            # Detectar tipo de transformación desde el nombre
            for t in ["color_map", "contrast", "hue", "saturation", "value", "texture"]:
                if t in filename:
                    with open(os.path.join(folder_path, filename), "r") as f:
                        vector = json.load(f)
                        data[t] = vector
    return data

# Cargar ambos conjuntos
emb1 = load_embeddings(EMB_DIR_1)
emb2 = load_embeddings(EMB_DIR_2)

# Comparar transformaciones equivalentes
print("🔍 Similitudes por transformación:")
results = {}

for key in emb1:
    if key in emb2:
        sim = cosine_similarity([emb1[key]], [emb2[key]])[0][0]
        results[key] = round(sim, 4)
        print(f"🟡 {key:<12} → Similitud: {sim:.4f}")
    else:
        print(f"⚠️ No se encontró la transformación '{key}' en la carpeta 2")

# (Opcional) Guardar en JSON
import json
with open("resultados_similitud_pca10.json", "w") as f:
    json.dump(results, f, indent=4)

print("\n✅ Comparación completada y guardada en 'resultados_similitud_pca10.json'")
