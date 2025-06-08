import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_file_to_cloudinary(file_path, public_id):
    result = cloudinary.uploader.upload(
        file_path,
        public_id=public_id,
        resource_type="raw", #  .json
        use_filename=False,
        unique_filename=False,
        overwrite=False
    )
    return result["secure_url"]
