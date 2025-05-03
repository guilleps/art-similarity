import cloudinary
import cloudinary.uploader
from api.infrastructure.exceptions import CloudinaryUploadError

def upload_image_to_cloudinary(image_file):
    try:
        result = cloudinary.uploader.upload(image_file)
        return { 'secure_url': result.get('secure_url') }
    except Exception as e:
        raise CloudinaryUploadError() from e
