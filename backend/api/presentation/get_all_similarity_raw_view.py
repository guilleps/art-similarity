from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.application.get_all_similarity_results_raw_usecase import (
    GetAllSimilarityResultsRawUseCase,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.infrastructure.config.tracker_to_emission import create_async_tracker


@extend_schema(
    summary="Get all similarity results (no pagination)",
    responses={200: OpenApiResponse(description="Returns all similarity results")},
)
class GetAllSimilarityResultsRawAPI(APIView):
    async def get(self, request, *args, **kwargs):
        tracker = create_async_tracker(filename="emissions_get_all_similarity_raw.csv")
        await tracker.start()

        try:
            use_case = GetAllSimilarityResultsRawUseCase()
            results = await use_case.execute_async()

            await tracker.stop_background()

            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            await tracker.stop_background()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
