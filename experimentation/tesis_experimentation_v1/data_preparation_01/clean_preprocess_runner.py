import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image, ExifTags

reader = easyocr.Reader(['en'], gpu=False)

def validate_image_array(image: np.ndarray) -> None:
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("[Error] Input no es una imagen válida.")

    # Convertir canal alfa si existe
    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Validar desenfoque
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if lap_var < 50:
        raise ValueError(f"[Error] Imagen borrosa (varianza: {lap_var:.2f})")

    return image

def detect_text(image: np.ndarray) -> bool:
    results = reader.readtext(image)
    return len(results) > 0

def correct_orientation(image_pil: Image.Image) -> Image.Image:
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image_pil.getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                image_pil = image_pil.rotate(180, expand=True)
            elif orientation_value == 6:
                image_pil = image_pil.rotate(270, expand=True)
            elif orientation_value == 8:
                image_pil = image_pil.rotate(90, expand=True)
    except Exception as e:
        print(f"[WARN] Error al corregir orientación: {e}")
    return image_pil

def preprocess_image_from_array(image_array: np.ndarray, show: bool = False) -> Dict[str, np.ndarray]:
    image = validate_image_array(image_array)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Recorte centrado
    height, width, _ = image_rgb.shape
    min_size = min(height, width)
    x = (width - min_size) // 2
    y = (height - min_size) // 2
    cropped = image_rgb[y:y + min_size, x:x + min_size]

    resized = cv2.resize(cropped, (224, 224))

    # if detect_text(resized):
    #     raise ValueError(f"[Error] Imagen contiene texto detectado (posible marca de agua)")

    normalized = resized.astype(np.float32) / 255.
    preprocessed = preprocess_input(normalized)

    if show:
        plt.imshow(resized)
        plt.title("Imagen Preprocesada")
        plt.axis('off')
        plt.show()

    return {
        'original': image_rgb,
        'cropped': cropped,
        'resized': resized,
        'preprocessed': preprocessed
    }


######


pil_image = Image.open("./akseli-gallen-kallela_poster-for-the-german-exposition-of-art-in-ateneum-1922.jpg")
pil_image = correct_orientation(pil_image)
image_np = np.array(pil_image)

processed = preprocess_image_from_array(image_np, show=True)

