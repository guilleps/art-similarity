from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from api.application.get_all_similarity_results_usecase import GetAllSimilarityResultsUseCase
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    summary="Get all similarity sessions and their results.",
    responses={
        200: OpenApiResponse(description="Returns a list of all comparison sessions with their similarity metrics."),
    }
)
class GetAllSimilarityResultsAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            paginator = PageNumberPagination()
            paginator.page_size = int(request.query_params.get("limit", 10))

            use_case = GetAllSimilarityResultsUseCase()
            full_data = use_case.execute()
            result_page = paginator.paginate_queryset(full_data, request)
            return paginator.get_paginated_response(result_page)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)