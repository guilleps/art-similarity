import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_contrast_enhancement(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    lab_eq = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

def apply_texture_direction(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    magnitude = cv2.magnitude(sobelx, sobely)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    return magnitude.astype(np.uint8)

def apply_color_distribution_map(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    heatmap = np.mean(img_rgb, axis=2)  # promedio por canal para estimar "densidad"
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    return plt.cm.plasma(heatmap.astype(np.uint8))  # puedes usar otros mapas: 'hot', 'jet', etc.

def apply_hsv_channels(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Escalar cada canal para visualización
    h_vis = cv2.normalize(h, None, 0, 255, cv2.NORM_MINMAX)
    s_vis = cv2.normalize(s, None, 0, 255, cv2.NORM_MINMAX)
    v_vis = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)

    return {
        "hue": h_vis.astype(np.uint8),
        "saturation": s_vis.astype(np.uint8),
        "value": v_vis.astype(np.uint8)
    }
