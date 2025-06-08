from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from api.domain.models import ImageComparisonSession

@extend_schema(
    summary="Get the next image comparison session.",
    parameters=[
        OpenApiParameter(
            name='current_id',
            type=str,
            location=OpenApiParameter.QUERY,
            description='Optional current session ID to determine the next session (if provided).'
        )
    ],
    responses={
        200: OpenApiResponse(description="Returns the next session's `comparison_id`, the total number of sessions, and the current index."),
        404: OpenApiResponse(description="No comparison sessions found."),
    }
)
class GetComparisonSessionAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Lista de IDs ordenada por fecha de creación
        sessions = [str(s) for s in ImageComparisonSession.objects.order_by('created_at').values_list('id', flat=True)]

        if not sessions:
            return Response({"error": "No hay sesiones registradas"}, status=status.HTTP_404_NOT_FOUND)

        # ID actual recibido por query param
        current_id = request.query_params.get("current_id")

        if current_id and current_id in map(str, sessions):
            current_index = sessions.index(current_id)
            next_index = (current_index + 1) % len(sessions)  # 🟡 ROTACIÓN aquí
        else:
            next_index = 0

        next_id = sessions[next_index]
        return Response({
            "comparison_id": str(next_id),
            "total": len(sessions),
            "current_index": next_index
        }, status=status.HTTP_200_OK)
