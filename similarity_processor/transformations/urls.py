from django.urls import path
from .presentation.upload_transform_view import UploadTransformedImagesAPI

urlpatterns = [
    path(
        "internal/upload-transform/",
        UploadTransformedImagesAPI.as_view(),
        name="upload_transform",
    ),
]
