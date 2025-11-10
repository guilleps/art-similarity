from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.domain.models import ImageComparisonSession
from api.application.get_similarity_results_pag_usecase import (
    GetSimilarityResultsPagUseCase,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from codecarbon import EmissionsTracker


@extend_schema(
    summary="Get all similarity sessions and their results.",
    responses={
        200: OpenApiResponse(
            description="Returns a list of all comparison sessions with their similarity metrics."
        ),
    },
)
class GetSimilarityResultsPagAPI(APIView):
    def get(self, request, *args, **kwargs):
        tracker = EmissionsTracker(
            project_name="ArtShift",
            experiment_id="e0f3a9ae-b84d-4bc3-bda2-0ff6ab5842a9",
            output_dir="./carbon_reports",
            output_file="emissions_get_all_similarity.csv",
        )
        tracker.start()

        try:
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 10))
            offset = (page - 1) * limit

            use_case = GetSimilarityResultsPagUseCase()
            paginated_data = use_case.execute(offset=offset, limit=limit)
            total = ImageComparisonSession.objects.count()

            tracker.stop()

            return Response(
                {"count": total, "results": paginated_data}, status=status.HTTP_200_OK
            )

        except Exception as e:
            tracker.stop()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
