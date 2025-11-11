from django.urls import path
from .presentation.get_similarity_view import GetSimilarityResultAPI
from .presentation.get_all_similarity_view import GetSimilarityResultsPagAPI
from .presentation.get_all_similarity_raw_view import GetAllSimilarityResultsRawAPI
from .presentation.get_similarity_by_transform_view import GetSimilarityByTransformAPI
from .presentation.export_similarity_results_view import ExportSimilarityResultsAPI


urlpatterns = [
    path(
        "get-similarity/<uuid:comparison_id>/",
        GetSimilarityResultAPI.as_view(),
        name="get_similarity_result",
    ),
    path(
        "get-all-similarities/",
        GetSimilarityResultsPagAPI.as_view(),
        name="get_all_similarity_results",
    ),
    path(
        "get-all-similarities/raw/",
        GetAllSimilarityResultsRawAPI.as_view(),
        name="get_all_similarity_results_raw",
    ),
    path(
        "get-similarity-by-transform/",
        GetSimilarityByTransformAPI.as_view(),
        name="get_similarity_by_transform",
    ),
    path(
        "export-similarity-results/json/",
        ExportSimilarityResultsAPI.as_view(),
        name="export_similarity_results_json",
    ),
    path(
        "export-similarity-results/csv/",
        ExportSimilarityResultsAPI.as_view(),
        name="export_similarity_results_csv",
    ),
]
