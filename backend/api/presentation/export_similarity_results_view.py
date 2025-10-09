from django.http import HttpResponse
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application.export_similarity_results_usecase import (
    ExportSimilarityResultsUseCase,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter


@extend_schema(
    summary="Export all similarity results",
    responses={
        200: OpenApiResponse(description="Exported data in the requested format"),
        404: OpenApiResponse(description="Format not supported"),
        500: OpenApiResponse(description="Internal server error"),
    },
)
class ExportSimilarityResultsAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            use_case = ExportSimilarityResultsUseCase()
            if request.path.endswith("/csv/"):
                format_type = "csv"
            elif request.path.endswith("/json/"):
                format_type = "json"

            if format_type == "csv":
                response = HttpResponse(
                    content_type="text/csv; charset=utf-8", status=200
                )
                response["Content-Disposition"] = (
                    'attachment; filename="similarity_results.csv"'
                )

                return use_case.exportToCSV(response_object=response)

            elif format_type == "json":
                data = use_case.exportToJSON()
                response = HttpResponse(
                    json.dumps(data, indent=2),
                    content_type="application/json",
                    status=200,
                )
                response["Content-Disposition"] = (
                    'attachment; filename="similarity_results.json"'
                )
                return response
            else:
                return Response(
                    {"error": "Invalid format. Use 'json' or 'csv'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
