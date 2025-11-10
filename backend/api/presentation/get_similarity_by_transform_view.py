from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from api.application import GetAllSimilarityResultsRawUseCase
from .serializers.similarity_by_transform_serializer import (
    SimilarityByTransformItemSerializer,
)
from api.infrastructure.config import create_tracker_to_emission


@extend_schema(
    summary="Obtain results by type of transformation",
    parameters=[
        OpenApiParameter(
            name="transform",
            required=True,
            type=str,
            description=(
                "Type of transformation applied to the image. Possible values:\n\n"
                "- `color_heat_map`: Mapa de calor de color (TMCC)\n"
                "- `tone`: Tono (TT)\n"
                "- `saturation`: Saturación (TS)\n"
                "- `brightness`: Brillo (TB)\n"
                "- `texture`: Textura (TX)\n"
                "- `contrast`: Contraste (TC)"
            ),
            enum=[
                "color_heat_map",
                "tone",
                "saturation",
                "brightness",
                "texture",
                "contrast",
            ],
        )
    ],
    responses={200: SimilarityByTransformItemSerializer(many=True)},
)
class GetSimilarityByTransformAPI(APIView):
    def get(self, request, *args, **kwargs):
        transform_type = request.query_params.get("transform")
        if not transform_type:
            return Response(
                {"error": "You must provide the ‘transform’ parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tracker = create_tracker_to_emission(filename="emissions_get_similarity_by_transform.csv")
        tracker.start()

        try:
            use_case = GetAllSimilarityResultsRawUseCase()
            all_results = use_case.execute()

            filtered = [
                {"pair": idx + 1, "value": item.get(f"{transform_type}_transformation")}
                for idx, item in enumerate(all_results)
                if item.get(f"{transform_type}_transformation") is not None
            ]

            tracker.stop()

            return Response(filtered, status=status.HTTP_200_OK)

        except Exception as e:
            tracker.stop()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
