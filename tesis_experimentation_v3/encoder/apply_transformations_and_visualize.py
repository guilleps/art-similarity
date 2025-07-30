import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

# === TRANSFORMACIÓN 1: AUMENTO DE CONTRASTE (Canal L) ===
def apply_contrast_enhancement(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    lab_eq = cv2.merge((l_eq, a, b))
    result = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

    params = {
        "Espacio de color": "BGR → LAB",
        "Canal usado": "L (luminosidad)",
        "Técnica": "cv2.equalizeHist"
    }
    return result, params

# === TRANSFORMACIÓN 2: DIRECCIÓN DE TEXTURA (Gradientes Sobel) ===
def apply_texture_direction(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    magnitude = cv2.magnitude(sobelx, sobely)
    norm = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    params = {
        "Conversión": "BGR → Grayscale",
        "Filtro": "Sobel X + Y",
        "Kernel": "5x5",
        "Normalización": "cv2.NORM_MINMAX"
    }
    return norm.astype(np.uint8), params

# === TRANSFORMACIÓN 3: MAPA DE CALOR DE COLOR (Media RGB) ===
def apply_color_distribution_map(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_rgb = np.mean(rgb, axis=2)
    norm = cv2.normalize(avg_rgb, None, 0, 255, cv2.NORM_MINMAX)
    colormap = plt.cm.plasma(norm.astype(np.uint8))[:, :, :3]

    params = {
        "Espacio de color": "BGR → RGB",
        "Reducción de canales": "Media RGB",
        "Normalización": "cv2.NORM_MINMAX",
        "Colormap aplicado": "plasma"
    }
    return (colormap * 255).astype(np.uint8), params

# === TRANSFORMACIÓN 4: CANALES HSV POR SEPARADO ===
def apply_hsv_channels(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    h_norm = cv2.normalize(h, None, 0, 255, cv2.NORM_MINMAX)
    s_norm = cv2.normalize(s, None, 0, 255, cv2.NORM_MINMAX)
    v_norm = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)

    params = {
        "Hue": {
            "Canal": "Hue",
            "Normalización": "cv2.NORM_MINMAX"
        },
        "Saturation": {
            "Canal": "Saturation",
            "Normalización": "cv2.NORM_MINMAX"
        },
        "Value": {
            "Canal": "Value",
            "Normalización": "cv2.NORM_MINMAX"
        }
    }

    return {
        "Hue": h_norm.astype(np.uint8),
        "Saturation": s_norm.astype(np.uint8),
        "Value": v_norm.astype(np.uint8)
    }, params

# === FUNCIÓN AUXILIAR ===
def dict_to_str(d):
    return "\n".join(f"{k}: {v}" for k, v in d.items())

# === VISUALIZACIÓN GENERAL ===
def visualize_transformations(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Imagen no encontrada: {image_path}")

    # CONTRASTE
    start = time.perf_counter()
    contrast_img, contrast_params = apply_contrast_enhancement(image)
    contrast_time = time.perf_counter() - start

    # TEXTURA
    start = time.perf_counter()
    texture_img, texture_params = apply_texture_direction(image)
    texture_time = time.perf_counter() - start

    # COLORMAP
    start = time.perf_counter()
    heatmap_img, heatmap_params = apply_color_distribution_map(image)
    heatmap_time = time.perf_counter() - start

    # HSV
    start = time.perf_counter()
    hsv_imgs, hsv_params = apply_hsv_channels(image)
    hsv_time = time.perf_counter() - start

    fig, axs = plt.subplots(2, 4, figsize=(24, 10))
    fig.suptitle("Transformaciones Visuales + Parámetros Técnicos", fontsize=18)

    axs[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axs[0, 0].set_title("Original")
    axs[0, 0].axis("off")

    axs[0, 1].imshow(cv2.cvtColor(contrast_img, cv2.COLOR_BGR2RGB))
    axs[0, 1].set_title(f"\nContraste\n{dict_to_str(contrast_params)}")
    axs[0, 1].axis("off")

    axs[0, 2].imshow(texture_img, cmap="gray")
    axs[0, 2].set_title(f"\nTextura\n{dict_to_str(texture_params)}")
    axs[0, 2].axis("off")

    axs[0, 3].imshow(heatmap_img)
    axs[0, 3].set_title(f"\nMapa de Color\n{dict_to_str(heatmap_params)}")
    axs[0, 3].axis("off")

    axs[1, 0].imshow(hsv_imgs["Hue"], cmap="hsv")
    axs[1, 0].set_title(f"\nHue\n{dict_to_str(hsv_params['Hue'])}")
    axs[1, 0].axis("off")

    axs[1, 1].imshow(hsv_imgs["Saturation"], cmap="gray")
    axs[1, 1].set_title(f"\nSaturation\n{dict_to_str(hsv_params['Saturation'])}")
    axs[1, 1].axis("off")

    axs[1, 2].imshow(hsv_imgs["Value"], cmap="gray")
    axs[1, 2].set_title(f"\nValue\n{dict_to_str(hsv_params['Value'])}")
    axs[1, 2].axis("off")

    axs[1, 3].axis("off")
    
    plt.tight_layout(h_pad=5.0, w_pad=2.0)
    plt.subplots_adjust(top=0.85) 
    plt.show()

    total_time = contrast_time + texture_time + heatmap_time + hsv_time
    average_time = total_time / 6  # porque HSV tiene 3 imágenes, una por canal

    print("\nTiempo por transformacion...")
    print(f"** Contraste (seg): {contrast_time:.4f}")
    print(f"** Textura (seg): {texture_time:.4f}")
    print(f"** Mapa de color (seg): {heatmap_time:.4f}")
    print(f"** Hue (seg): {hsv_time/3:.4f}")  # dividido entre 3 porque aplica a H, S, V
    print(f"** Saturation (seg): {hsv_time/3:.4f}")
    print(f"** Value (seg): {hsv_time/3:.4f}")
    print(f"\nTiempo promedio por transformación (seg): {average_time:.4f}")


# --- Ejecutar ---
if __name__ == "__main__":
    image_file = r"C:\workspace\tesis_project\experimentation\tesis_experimentation_v1\sprint_1\similares\antoine-blanchard_arc-de-triomphe.jpg"  # ← reemplaza esto
    visualize_transformations(image_file)
