from django.urls import path
from api.presentation import UploadTransformedImagesAPI, GetSimilarityResultAPI

urlpatterns = [
    path('api/internal/upload-transform/', UploadTransformedImagesAPI.as_view(), name='upload_transform'),
    path('api/internal/get-similarity/<uuid:comparison_id>/', GetSimilarityResultAPI.as_view(), name='get_similarity_result'),
]
