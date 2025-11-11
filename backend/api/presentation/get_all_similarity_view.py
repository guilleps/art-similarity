from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.domain.models import ImageComparisonSession
from api.application.get_similarity_results_pag_usecase import (
    GetSimilarityResultsPagUseCase,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.infrastructure.config.tracker_to_emission import create_async_tracker


@extend_schema(
    summary="Get all similarity sessions and their results.",
    responses={
        200: OpenApiResponse(
            description="Returns a list of all comparison sessions with their similarity metrics."
        ),
    },
)
class GetSimilarityResultsPagAPI(APIView):
    async def get(self, request, *args, **kwargs):
        tracker = create_async_tracker(filename="emissions_get_all_similarity.csv")
        await tracker.start()

        try:
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 10))
            offset = (page - 1) * limit

            use_case = GetSimilarityResultsPagUseCase()
            paginated_data = await use_case.execute(offset=offset, limit=limit)

            total = await ImageComparisonSession.objects.acount()

            await tracker.stop_background()

            return Response(
                {"count": total, "results": paginated_data}, status=status.HTTP_200_OK
            )

        except Exception as e:
            await tracker.stop_background()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
