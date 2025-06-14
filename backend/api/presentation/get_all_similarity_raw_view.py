from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application.get_all_similarity_results_raw_usecase import GetAllSimilarityResultsRawUseCase
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    summary="Get all similarity results (no pagination)",
    responses={200: OpenApiResponse(description="Returns all similarity results")}
)
class GetAllSimilarityResultsRawAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            use_case = GetAllSimilarityResultsRawUseCase()
            results = use_case.execute()
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)