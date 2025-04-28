
from django.urls import path
from api.presentation import UploadImageAPI, UploadBatchAPI

urlpatterns = [
    path('api/upload/', UploadImageAPI.as_view(), name='upload_image'),
    path('api/upload-batch/', UploadBatchAPI.as_view(), name='upload_image_batch'),
]

