import pytest
import cloudinary.uploader
from api.infrastructure.services import CloudStorageService
from api.infrastructure.exceptions import CloudinaryUploadError

def test_upload_images_success(mocker):
    # Mockear el método interno de subida
    mocker.patch.object(
        CloudStorageService,
        'upload_image_to_cloudinary',
        side_effect=[
            {'secure_url': 'https://cloud/a.png'},
            {'secure_url': 'https://cloud/b.jpg'}
        ]
    )

    svc = CloudStorageService()
    urls = svc.upload_images(['a.png', 'b.jpg'])

    # Verificaciones
    assert urls == ['https://cloud/a.png', 'https://cloud/b.jpg']
    assert svc.upload_image_to_cloudinary.call_count == 2

def test_upload_image_to_cloudinary_success(mocker):

    mocker.patch.object(
        cloudinary.uploader,
        'upload',
        return_value={'secure_url': 'https://cloud/test.png'}
    )

    svc = CloudStorageService()
    result = svc.upload_image_to_cloudinary('file.png')

    assert result == {'secure_url': 'https://cloud/test.png'}

def test_upload_image_to_cloudinary_failure(mocker):

    mocker.patch.object(
        cloudinary.uploader,
        'upload',
        side_effect=Exception("API down")
    )

    svc = CloudStorageService()
    with pytest.raises(CloudinaryUploadError):
        svc.upload_image_to_cloudinary('file.png')