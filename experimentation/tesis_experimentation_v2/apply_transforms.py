# individal por imagen
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels
)

# Ruta de la imagen original
image_path = 'C:/workspace/deep_learning/filters/images/anders-zorn_in-the-studio-1896.jpg'
image_name = os.path.splitext(os.path.basename(image_path))[0]

# Carpeta de salida
output_dir = os.path.join('transformed_images', image_name)
os.makedirs(output_dir, exist_ok=True)

# Cargar imagen original
original = cv2.imread(image_path)

# Filtro de CONTRASTE (realce de luminancia)
contrast = apply_contrast_enhancement(original)
cv2.imwrite(os.path.join(output_dir, f"{image_name}_contrast.jpg"), contrast)

# TEXTURA o dirección de trazo (estimación por gradiente direccional)
texture = apply_texture_direction(original)
cv2.imwrite(os.path.join(output_dir, f"{image_name}_texture_direction.jpg"), texture)

# MAPA DE CALOR de distribución de colores
color_map = apply_color_distribution_map(original)
plt.imsave(os.path.join(output_dir, f"{image_name}_color_heatmap.jpg"), color_map)

# ESPACIO DE COLOR HSV
hsv_dict = apply_hsv_channels(original)
for name, img in hsv_dict.items():
    cv2.imwrite(os.path.join(output_dir, f"{image_name}_hsv_{name}.jpg"), img)

print(f"Transformaciones guardadas en {output_dir}")
