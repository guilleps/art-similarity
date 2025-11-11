from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from api.application import GetSimilarityResultUseCase
from api.infrastructure.config.tracker_to_emission import create_async_tracker
from asgiref.sync import sync_to_async


@extend_schema(
    summary="Get the similarity results of a specific pair of images.",
    parameters=[
        OpenApiParameter(
            name="comparison_id",
            type=str,
            location=OpenApiParameter.PATH,
            description="The unique ID of the comparison session.",
            required="comparison_id",
        ),
    ],
    responses={
        200: OpenApiResponse(
            description="Similarity results of the two images are returned, including comparison details."
        ),
        404: OpenApiResponse(
            description="The `comparison_id` was not found, or the session does not exist."
        ),
    },
)
class GetSimilarityResultAPI(APIView):
    async def get(self, request, comparison_id, *args, **kwargs):
        tracker = create_async_tracker(filename="emissions_get_similarity.csv")
        await tracker.start()

        try:
            use_case = GetSimilarityResultUseCase()
            result = await sync_to_async(use_case.execute)(comparison_id)

            await tracker.stop_background()

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            await tracker.stop_background()
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
