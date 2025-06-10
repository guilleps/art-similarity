from django.urls import path
from api.presentation import UploadTransformedImagesAPI, GetSimilarityResultAPI, GetComparisonSessionAPI, GetAllSimilarityResultsAPI

urlpatterns = [
    path('api/internal/upload-transform/', UploadTransformedImagesAPI.as_view(), name='upload_transform'),
    path('api/get-similarity/<uuid:comparison_id>/', GetSimilarityResultAPI.as_view(), name='get_similarity_result'),
    path('api/get-session/', GetComparisonSessionAPI.as_view(), name='session'),
    path('api/get-all-similarities/', GetAllSimilarityResultsAPI.as_view(), name='get_all_similarity_results')
]