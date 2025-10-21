import cv2
import numpy as np
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

def apply_contrast_enhancement(image):
    """Apply contrast enhancement to the input image."""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    lab_eq = cv2.merge((l_eq, a, b))
    logger.info('Applied transformation: contrast enhancement')
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

def apply_texture_direction(image):
    """Extract texture direction using Sobel operators."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    magnitude = cv2.magnitude(sobelx, sobely)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    logger.info('Applied transformation: texture direction')
    return magnitude.astype(np.uint8)

def apply_color_distribution_map(image):
    """Generate a color distribution heatmap."""
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    heatmap = np.mean(img_rgb, axis=2)  # Average across channels to estimate "density"
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    logger.info('Applied transformation: color distribution map')
    return plt.cm.plasma(heatmap.astype(np.uint8))

def apply_hsv_channels(image):
    """Extract and normalize individual HSV channels."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Normalize each channel for visualization
    h_vis = cv2.normalize(h, None, 0, 255, cv2.NORM_MINMAX)
    s_vis = cv2.normalize(s, None, 0, 255, cv2.NORM_MINMAX)
    v_vis = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)

    logger.info('Applied transformation: HSV channels')
    return {
        "hue": h_vis.astype(np.uint8),
        "saturation": s_vis.astype(np.uint8),
        "value": v_vis.astype(np.uint8)
    }