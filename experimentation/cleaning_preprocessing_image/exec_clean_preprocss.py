import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict

def preprocess_image(path: str, show: bool = True) -> Dict[str, np.ndarray]:
    imageCV2 = cv2.imread('./a-y-jackson_a-copse-evening-1918.jpg')
    if imageCV2 is None:
        raise ValueError(f"Upload error image: {imageCV2}")

    gray = cv2.cvtColor(imageCV2, cv2.COLOR_BGR2GRAY) # conversion a grises

    resizedCV2 = cv2.resize(imageCV2, (224,224)) #redimension

    # recorte centrado de imagen
    height, width, _ = imageCV2.shape
    size = min (height, width)
    x = (width - size) // 2
    y = (height - size) // 2
    croppedCV2 = imageCV2[y: y+size, x: x+size]

    normalizedCV2 = imageCV2.astype(np.float32) / 255. # normalizado 0.0 - 1.0

    eq_img = cv2.equalizeHist(gray) # ecualiza histograma

    # estandariacion por canal
    mean, std = cv2.meanStdDev(imageCV2)
    mean = mean.reshape((1, 1, 3))
    std = std.reshape((1, 1, 3))

    std_img = (imageCV2.astype(np.float32) - mean) / (std + 1e-8)

    # Convertir de BGR a RGB para mostrar bien con matplotlib
    image_rgb = cv2.cvtColor(imageCV2, cv2.COLOR_BGR2RGB)
    resized_rgb = cv2.cvtColor(resizedCV2, cv2.COLOR_BGR2RGB)
    cropped_rgb = cv2.cvtColor(croppedCV2, cv2.COLOR_BGR2RGB)
    normalized_rgb = cv2.cvtColor((normalizedCV2 * 255).astype(np.uint8), cv2.COLOR_BGR2RGB)
    std_rgb = cv2.cvtColor(np.clip((std_img * 50 + 128), 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)

    # visualizacion del proceso de la imagen
    titles = ['Original', 'Redimensionada', 'Centrada', 'Normalizada', 'Estandarizada', 'Ecualizada']
    images = [image_rgb, resized_rgb, cropped_rgb, normalized_rgb, std_rgb, eq_img]

    plt.figure(figsize=(18, 5))
    for i in range(len(images)):
        plt.subplot(1, 6, i + 1)

        if len(images[i].shape) == 2: # solo en caso de gray escala
            plt.imshow(images[i], cmap='gray')
        else:
            plt.imshow(images[i])
        plt.title(titles[i])
        plt.axis('off')
    plt.tight_layout()
    plt.show()
