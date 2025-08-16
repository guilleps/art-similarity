import os
import cv2
from tqdm import tqdm
from utils_transformations import apply_contrast_enhancement, apply_texture_direction, apply_color_distribution_map, apply_hsv_channels
import matplotlib.pyplot as plt

def save_transform(img_path, out_dir):
    image = cv2.imread(img_path)
    if image is None: 
        print(f"No se puede leer: {img_path}")
        return
    
    base_name = os.path.splitext(os.path.basename(img_path))[0] # obtiene nombre de img

    cv2.imwrite(os.path.join(out_dir, f"{base_name}_original.jpg"), image) # guarda img_original

    contrast = apply_contrast_enhancement(image)
    cv2.imwrite(os.path.join(out_dir, f"{base_name}_constrast.jpg"), contrast) # guarda img_contrast

    texture = apply_texture_direction(image)
    cv2.imwrite(os.path.join(out_dir, f"{base_name}_texture.jpg"), texture) # guarda img_Textura

    heatmap = apply_color_distribution_map(image)
    plt.imsave(os.path.join(out_dir, f"{base_name}_heatmap.jpg"), heatmap) # guarda img_Mapa de calor

    hsv = apply_hsv_channels(image)
    for channel, img in hsv.items():
        cv2.imwrite(os.path.join(out_dir, f"{base_name}_hsv_{channel}.jpg"), img) # guarda img_HSV

def process_folder(input_folder, out_dir):
    image_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    
    for img_file in tqdm(image_files, desc="Procesando images"):
        full_path = os.path.join(input_folder, img_file)
        save_transform(full_path, out_dir)
        
if __name__ == "__main__":
    input_dir = r"C:\workspace\data\train\impressionism"
    output_dir = r"C:\data_transformed"
    
    os.makedirs(output_dir, exist_ok=True)
    process_folder(input_dir, output_dir)
