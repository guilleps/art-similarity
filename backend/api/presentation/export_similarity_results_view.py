from django.http import HttpResponse
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application.export_similarity_results_usecase import (
    ExportSimilarityResultsUseCase,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from codecarbon import EmissionsTracker


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
        tracker = EmissionsTracker(
            project_name="ArtShift",
            experiment_id="e0f3a9ae-b84d-4bc3-bda2-0ff6ab5842a9",
            output_dir="./carbon_reports",
            output_file="emissions_export.csv",
        )
        tracker.start()

        try:
            use_case = ExportSimilarityResultsUseCase()

            if request.path.endswith("/csv/"):
                format_type = "csv"
            elif request.path.endswith("/json/"):
                format_type = "json"
            else:
                return Response(
                    {"error": "Invalid format. Use 'json' or 'csv'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if format_type == "csv":
                response = HttpResponse(
                    content_type="text/csv; charset=utf-8", status=status.HTTP_200_OK
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
                    status=status.HTTP_200_OK,
                )
                response["Content-Disposition"] = (
                    'attachment; filename="similarity_results.json"'
                )
                return response
                
            tracker.stop()
        except Exception as e:
            tracker.stop()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
