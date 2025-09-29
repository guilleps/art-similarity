import cv2
from tqdm import tqdm
from utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels,
)
import matplotlib.pyplot as plt
from pathlib import Path
import os


def save_transform(img_path, out_dir):
    """Aplica y guarda todas las transformaciones de una imagen"""
    image = cv2.imread(img_path)
    if image is None:
        print(f"No se puede leer: {img_path}")
        return

    base_name = os.path.splitext(os.path.basename(img_path))[0]

    # Guarda imagen original
    cv2.imwrite(os.path.join(out_dir, f"{base_name}_original.jpg"), image)

    # Guarda contraste
    contrast = apply_contrast_enhancement(image)
    cv2.imwrite(os.path.join(out_dir, f"{base_name}_contrast.jpg"), contrast)

    # Guarda textura
    texture = apply_texture_direction(image)
    cv2.imwrite(os.path.join(out_dir, f"{base_name}_texture.jpg"), texture)

    # Guarda mapa de calor
    heatmap = apply_color_distribution_map(image)
    plt.imsave(os.path.join(out_dir, f"{base_name}_heatmap.jpg"), heatmap)

    # Guarda canales HSV
    hsv = apply_hsv_channels(image)
    for channel, img in hsv.items():
        cv2.imwrite(os.path.join(out_dir, f"{base_name}_hsv_{channel}.jpg"), img)


def process_numbered_folders(input_base_dir, output_base_dir):
    """
    Procesa todas las carpetas numeradas dentro de input_base_dir
    y guarda las transformaciones en output_base_dir
    """
    input_path = Path(input_base_dir)
    output_path = Path(output_base_dir)

    # Verifica que exista la carpeta de entrada
    if not input_path.exists():
        print(f"Error: La carpeta {input_base_dir} no existe")
        return

    # Obtiene todas las carpetas numeradas (1-100)
    numbered_folders = []
    for folder in input_path.iterdir():
        if folder.is_dir() and folder.name.isdigit():
            folder_num = int(folder.name)
            if 1 <= folder_num <= 100:
                numbered_folders.append(folder)

    # Ordena las carpetas por número
    numbered_folders.sort(key=lambda x: int(x.name))

    print(f"Se encontraron {len(numbered_folders)} carpetas numeradas para procesar")

    # Procesa cada carpeta numerada
    for folder in tqdm(numbered_folders, desc="Procesando carpetas"):
        folder_name = folder.name

        # Crea la carpeta de salida correspondiente
        output_folder = output_path / folder_name
        os.makedirs(output_folder, exist_ok=True)

        # Obtiene todas las imágenes en la carpeta
        image_files = [
            f
            for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg"]
        ]

        # Procesa cada imagen
        for img_file in image_files:
            save_transform(str(img_file), str(output_folder))

    print(f"\n✓ Procesamiento completado")
    print(f"Resultados guardados en: {output_base_dir}")


if __name__ == "__main__":
    # Define las rutas de entrada y salida
    input_directory = Path("/home/guille/workspace/pairs")
    output_directory = Path("/home/guille/workspace/pairs_transformation")

    # Ejecuta el procesamiento
    process_numbered_folders(input_directory, output_directory)
