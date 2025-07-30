import os
import json
import matplotlib.pyplot as plt

# Ruta base
base_path = "."
model = "efficientnetb2"
transformations = ["heat_color_map", "contrast", "hsv_hue", "hsv_saturation", "hsv_value", "texture"]

results = {t: [] for t in transformations}

# Leer resultados de B0
model_path = os.path.join(base_path, model)
json_files = sorted([f for f in os.listdir(model_path) if f.endswith(".json")])

for json_file in json_files:
    with open(os.path.join(model_path, json_file), 'r') as f:
        data = json.load(f)
        for t in transformations:
            results[t].append(data[t]["similarity"])

# Etiquetas del eje X: Par 1, Par 2, ...
num_pares = len(json_files)
x_labels = [f'Par {i+1}' for i in range(num_pares)]
x = list(range(num_pares))

# Crear figura
plt.figure(figsize=(12, 6))

# Trazar cada transformación
for t in transformations:
    plt.plot(x, results[t], marker='o', label=f'{t}')

plt.xticks(ticks=x, labels=x_labels)
plt.title('Similitud por transformación – EfficientNetB2')
plt.xlabel('Par de imágenes')
plt.ylabel('Similitud (0 a 1)')
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
