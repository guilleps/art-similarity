import os
import cloudinary
import cloudinary.uploader

CLOUDINARY_CLOUD_NAME = ""
CLOUDINARY_API_KEY = ""
CLOUDINARY_API_SECRET = ""

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
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
