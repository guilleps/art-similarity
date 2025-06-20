from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application.export_similarity_results_usecase import ExportSimilarityResultsUseCase
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    summary="Exportar todos los resultados de similitud como JSON estructurado",
    responses={200: OpenApiResponse(description="JSON estructurado con resultados de similitud por par")}
)
class ExportSimilarityResultsAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            use_case = ExportSimilarityResultsUseCase()
            json_data = use_case.execute()
            return Response(json_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

