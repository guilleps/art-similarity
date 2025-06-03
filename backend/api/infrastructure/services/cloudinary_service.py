import os
import cloudinary
import cloudinary.uploader
from api.infrastructure.exceptions import CloudinaryUploadError

class CloudStorageService:
    def upload_images(self, local_path: str, filenames: list[str]) -> list[str]:
        urls = []
        for file in filenames:
            full_path = os.path.join(local_path, file)
            result = self.upload_image_to_cloudinary(full_path)
            urls.append(result["secure_url"])
        return urls
    
    def upload_image_to_cloudinary(self, image_file):
        try:
            result = cloudinary.uploader.upload(image_file)
            return { 'secure_url': result.get('secure_url') }
        except Exception as e:
            raise CloudinaryUploadError() from e
    