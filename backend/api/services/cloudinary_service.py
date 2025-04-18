import cloudinary
import cloudinary.uploader

def upload_image_to_cloudinary(image_file):
    result = cloudinary.uploader.upload(image_file)
    return {
        'url': result.get('url'),
        'secure_url': result.get('secure_url')
    }