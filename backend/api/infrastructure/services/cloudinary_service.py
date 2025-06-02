import cloudinary
import cloudinary.uploader
from api.infrastructure.exceptions import CloudinaryUploadError

def upload_image_to_cloudinary(image_file):
    try:
        result = cloudinary.uploader.upload(image_file)
        return { 'secure_url': result.get('secure_url') }
    except Exception as e:
        raise CloudinaryUploadError() from e

def upload_file_to_cloudinary(file_path):
    try:
        result = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",  # para archivos .json
            use_filename=True,
            unique_filename=False,
            overwrite=True
        )
        return { 'secure_url': result.get('secure_url') }
    except Exception as e:
        raise CloudinaryUploadError(f"Error al subir {file_path} a Cloudinary") from e
