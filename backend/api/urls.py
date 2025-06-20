from django.urls import path
from api.presentation import (
    UploadTransformedImagesAPI,
    GetSimilarityResultAPI,
    GetSimilarityResultsPagAPI,
    GetAllSimilarityResultsRawAPI,
    GetSimilarityByTransformAPI,
    ExportSimilarityResultsAPI
)

urlpatterns = [
    path('api/internal/upload-transform/', UploadTransformedImagesAPI.as_view(), name='upload_transform'),
    path('api/get-similarity/<uuid:comparison_id>/', GetSimilarityResultAPI.as_view(), name='get_similarity_result'),
    path('api/get-all-similarities/', GetSimilarityResultsPagAPI.as_view(), name='get_all_similarity_results'),
    path('api/get-all-similarities/raw/', GetAllSimilarityResultsRawAPI.as_view(), name='get_all_similarity_results_raw'),
    path('api/get-similarity-by-transform/', GetSimilarityByTransformAPI.as_view(), name='get_similarity_by_transform'),
    path('api/export-similarity-results/', ExportSimilarityResultsAPI.as_view(), name='export_similarity_results')
]