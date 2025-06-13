from django.urls import path
from api.presentation import UploadTransformedImagesAPI, GetSimilarityResultAPI, GetAllSimilarityResultsAPI, GetSimilarityByTransformAPI

urlpatterns = [
    path('api/internal/upload-transform/', UploadTransformedImagesAPI.as_view(), name='upload_transform'),
    path('api/get-similarity/<uuid:comparison_id>/', GetSimilarityResultAPI.as_view(), name='get_similarity_result'),
    path('api/get-all-similarities/', GetAllSimilarityResultsAPI.as_view(), name='get_all_similarity_results'),
    path('api/get-similarity-by-transform/', GetSimilarityByTransformAPI.as_view(), name='get_similarity_by_transform')
]