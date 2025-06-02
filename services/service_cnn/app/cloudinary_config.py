import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(image_path):
    result = cloudinary.uploader.upload(image_path)
    return result["secure_url"]

def upload_file_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(
        file_path,
        resource_type="raw", #  .json
        use_filename=True,
        unique_filename=False,
        overwrite=True
    )
    return result["secure_url"]
