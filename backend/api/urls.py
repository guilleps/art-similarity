
from django.urls import path
from .views.views import UploadImageAPI, UploadImageBatchAPI

urlpatterns = [
    path('api/upload/', UploadImageAPI.as_view(), name='upload_image'),
    path('api/upload-batch/', UploadImageBatchAPI.as_view(), name='upload_image_batch'),
]

