import os
import cv2
from matplotlib import pyplot as plt
from uuid import uuid4
import requests
import tempfile
from .utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels,
)
from .cloudinary_service import CloudStorageService


class TransformationService:
    def __init__(self):
        self.cloudinary_service = CloudStorageService()

    def transform_images(self, image_1_url: str, image_2_url: str) -> dict:
        results = {}

        for idx, (label, url) in enumerate(
            [("image_1", image_1_url), ("image_2", image_2_url)], start=1
        ):
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise Exception(f"Error downloading image {label}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                temp_path = tmp_file.name

            try:
                transformed_urls = self.save_transformed_images(
                    temp_path, "/tmp/outputs"
                )
                transformed_urls["original_image"] = url
                results[label] = transformed_urls
            finally:
                os.remove(temp_path)

        return results

    def save_transformed_images(self, image_path: str, output_dir: str) -> dict:
        image = cv2.imread(image_path)
        name = os.path.splitext(os.path.basename(image_path))[0]
        transformed_dir = os.path.join(output_dir, f"{name}_{uuid4().hex[:8]}")
        os.makedirs(transformed_dir, exist_ok=True)

        result_urls = {}

        def save_and_upload(suffix, img):
            filename = f"{name}_{suffix}.jpg"
            full_path = os.path.join(transformed_dir, filename)
            cv2.imwrite(full_path, img)
            upload_resp = self.cloudinary_service.upload_image_to_cloudinary(full_path)
            result_urls[suffix] = upload_resp['secure_url']

        save_and_upload("contrast", apply_contrast_enhancement(image))
        save_and_upload("texture", apply_texture_direction(image))

        color_map_path = os.path.join(transformed_dir, f"{name}_color_map.jpg")
        plt.imsave(color_map_path, apply_color_distribution_map(image))
        upload_resp = self.cloudinary_service.upload_image_to_cloudinary(color_map_path)
        result_urls["heat_color_map"] = upload_resp["secure_url"]

        hsv_channels = apply_hsv_channels(image)
        for channel, img in hsv_channels.items():
            save_and_upload(f"hsv_{channel}", img)

        return result_urls
