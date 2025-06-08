import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_API_SECRET"],
    secure=True
)

def upload_image(image_path):
    result = cloudinary.uploader.upload(image_path)
    return result["secure_url"]
