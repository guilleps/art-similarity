import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Raíz donde están tus carpetas 6 a 10
ROOT = Path("images")

# Define las carpetas similares y no similares
carpetas_similares = {"6", "8", "9"}
carpetas_no_similares = {"7", "11", "12"}

similares_global = []
no_similares_global = []

# Recorremos carpetas 6 a 10
for carpeta in (ROOT / str(i) for i in range(6, 11)):
    resultados_path = carpeta / "embeddings"
    if not resultados_path.exists():
        continue

    for json_path in resultados_path.rglob("resultados_similitud.json"):
        with open(json_path) as f:
            data = json.load(f)

        for tipo, valores in data.items():
            similarity = valores.get("similarity")
            if similarity is not None:
                if carpeta.name in carpetas_similares:
                    similares_global.append(similarity)
                elif carpeta.name in carpetas_no_similares:
                    no_similares_global.append(similarity)

# Calcular promedios reales
global_similar_avg = np.mean(similares_global)
global_nonsimilar_avg = np.mean(no_similares_global)
diferencia = global_similar_avg - global_nonsimilar_avg

# Mostrar en consola para informe
print("✅ TA-11 y TA-12:")
print(f"Promedio Similares: {global_similar_avg:.4f}")
print(f"Promedio No Similares: {global_nonsimilar_avg:.4f}")
print(f"Diferencia: {diferencia:.4f}")

# Graficar
labels = ['Similares', 'No Similares']
valores = [global_similar_avg, global_nonsimilar_avg]
colors = ['blue', 'orange']

plt.figure(figsize=(6, 5))
bars = plt.bar(labels, valores, color=colors)
plt.ylim(0, 1)
plt.ylabel("Similitud coseno promedio")
plt.title("Comparación global entre pares similares y no similares")

# Mostrar valores sobre cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.2f}", ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()
