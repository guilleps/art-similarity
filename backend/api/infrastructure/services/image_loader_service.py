import os

class ImageLoaderService:
    def load_images(self, local_path: str) -> list[str]:
        image_files = [f for f in os.listdir(local_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if len(image_files) != 2:
            raise ValueError("Se requieren exactamente dos imágenes en la carpeta.")
        return sorted(image_files)