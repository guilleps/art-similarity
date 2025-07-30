import os
import json
import plotly.graph_objects as go

base_path = "images"

label_map = {
    "heat_color_map": "Heat Color Map",
    "contrast": "Contrast",
    "hsv_hue": "Hue",
    "hsv_saturation": "Saturation",
    "hsv_value": "Value (Luminance)",
    "texture": "Texture"
}

all_results_dict = {}

# extrae los .json de cada par
for folder in sorted(os.listdir(base_path)):
    result_path = os.path.join(base_path, folder, "embeddings", "resultados_similitud.json")
    if os.path.exists(result_path):
        with open(result_path, "r") as f:
            all_results_dict[folder] = json.load(f)

fig = go.Figure()

for folder, data in all_results_dict.items():
    fig.add_trace(go.Scatter(
        x=[label_map.get(k, k) for k in data.keys()],
        y=[v["similarity"] for v in data.values()],
        mode='lines+markers',
        name=f"Par N°{folder}"
    ))

fig.update_layout(
    title='Similitud por Transformación Visual (Interactivo)',
    xaxis_title='Transformación',
    yaxis_title='Similitud (Coseno)',
    yaxis=dict(range=[0.8, 1.0]),
    hovermode='x unified'
)

fig.show()