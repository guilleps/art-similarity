from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from api.application import GetAllSimilarityResultsUseCase

@extend_schema(
    summary="Obtener resultados por tipo de transformación",
    parameters=[OpenApiParameter(name="transform", required=True, type=str)],
    responses={200: ...}
)
class GetSimilarityByTransformAPI(APIView):
    def get(self, request, *args, **kwargs):
        transform_type = request.query_params.get("transform")
        if not transform_type:
            return Response({"error": "Debe proporcionar el parámetro 'transform'"}, status=400)

        use_case = GetAllSimilarityResultsUseCase()
        all_results = use_case.execute()

        filtered = [
            {
                "par": idx + 1,
                "value": item.get(f"{transform_type}_transformation")
            }
            for idx, item in enumerate(all_results)
            if item.get(f"{transform_type}_transformation") is not None
        ]

        return Response(filtered, status=200)
