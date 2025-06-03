import os
import cv2
from app.utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels
)
from matplotlib import pyplot as plt
from uuid import uuid4
from app.cloudinary_config import upload_image

def save_transformed_images(image_path: str, output_dir: str) -> str:
    image = cv2.imread(image_path)
    name = os.path.splitext(os.path.basename(image_path))[0]
    transformed_dir = os.path.join(output_dir, f"{name}_{uuid4().hex[:8]}")
    os.makedirs(transformed_dir, exist_ok=True)

    result_urls = {}

    def save_and_upload(suffix, img):
        filename = f"{name}_{suffix}.jpg"
        full_path = os.path.join(transformed_dir, filename)
        cv2.imwrite(full_path, img)
        result_urls[suffix] = upload_image(full_path)

    save_and_upload("contrast", apply_contrast_enhancement(image))
    save_and_upload("texture", apply_texture_direction(image))
    plt.imsave(os.path.join(transformed_dir, f"{name}_color_map.jpg"),
               apply_color_distribution_map(image))
    result_urls["heat_color_map"] = upload_image(os.path.join(transformed_dir, f"{name}_color_map.jpg"))

    hsv_channels = apply_hsv_channels(image)
    for channel, img in hsv_channels.items():
        save_and_upload(f"hsv_{channel}", img)

    return result_urls
