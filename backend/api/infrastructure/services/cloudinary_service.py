import os
import cloudinary
import cloudinary.uploader
from api.infrastructure.exceptions import CloudinaryUploadError

class CloudStorageService:
    def upload_images(self, images) -> list[str]:
        urls = []
        for image in images:
            result = self.upload_image_to_cloudinary(image)
            urls.append(result["secure_url"])
        return urls
    
    def upload_image_to_cloudinary(self, image_file):
        try:
            result = cloudinary.uploader.upload(image_file)
            return { 'secure_url': result.get('secure_url') }
        except Exception as e:
            raise CloudinaryUploadError() from e
    